from flask import request, jsonify, Blueprint, json
from api.models import User, Product
from api.validator import ValidateUser, ValidateProduct
from database.db import DatabaseConnection
from flask_jwt_extended import (create_access_token,
                                get_jwt_identity, jwt_required)
import datetime

db = DatabaseConnection()


blueprint = Blueprint('application', __name__)


@blueprint.route('/signup', methods=['POST'])
def signup():
    """
    Function enables user to create an account on the platform.
    :returns:
    A success message upon successful registeration
    """
    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    user = ValidateUser(username, email, password)

    if not user.validate_username():
        return jsonify({
            'message': 'Username cannot be empty or contain numbers!'
        }), 400
    elif not user.validate_email():
        return jsonify({
            'message': 'Email cannot be empty and must be in the form \
(john.doe@example.com)'
        }), 400
    elif not user.validate_password():
        return jsonify({
            'message': 'Password should contain at least one uppercase, \
lowercase and number characcters and must be longer than 5 characters!'
        }), 400
    elif Product.query('users', 'username', username):
        return jsonify({
            'message': 'This username is already taken!'
        }), 400
    elif Product.query('users', 'email', email):
        return jsonify({
            'message': 'This email is already taken!'
        }), 400
    user = User(username, email, password)
    hashed_password = user.generate_hash()
    user = User(username, email, hashed_password)
    username = user.insert_user()

    return jsonify({
        'message': '{} successfully registered!'.format(username)
    }), 201


@blueprint.route('/login', methods=['POST'])
def login():
    """
    Function enables user to log into their account.
    :returns:
    A token and a success message
    """
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    user = ValidateUser(username, False, password)

    if not user.validate_username() or not password or password.isspace():
        return jsonify({
            'message': 'One of the required fields is empty!'
        }), 400
    elif not Product.query('users', 'username', username):
        return jsonify({
            'message': 'Sorry wrong username!'
        }), 400
    elif not User.verify_password(username, password):
        return jsonify({
            'message': 'Sorry wrong password!'
        }), 400
    token = create_access_token(identity=username)
    return jsonify({
        'token': token,
        'message': 'Logged in!'
    }), 200


@blueprint.route('/products', methods=['POST'])
@jwt_required
def add_product():
    """
    Function adds a product to the products list.
    :returns:
    A success message and the product.
    """
    username = get_jwt_identity()
    user = Product.query('users', 'username', username)

    if user[-1] is False:
        return jsonify({
            'message': 'You are not authorized to access this!'
        }), 503
    try:
        data = request.get_json()

        name = data.get('name')
        quantity = data.get('quantity')
        unit_price = data.get('unit_price')

        quantity = int(quantity)
        unit_price = int(unit_price)

        validate_product = ValidateProduct(name, quantity, unit_price)
        product = Product(name, quantity, unit_price)
        if validate_product.validate() is False:
            return jsonify({
                'message': 'One of the required fields is empty!'
            }), 400
        product_dict = product.insert_product()
        if not product_dict:
            return jsonify({
                'message': 'This product already exists!'
            }), 400
        return jsonify({
            'product': product_dict,
            'message': 'Product added successfully!'
        }), 201
    except ValueError:
        return jsonify({
            'message': 'The unit price and quantity must be numbers!'
        }), 400


@blueprint.route('/products/<product_id>', methods=['DELETE'])
@jwt_required
def delete_product(product_id):
    """
    Function enables user to delete a product from the database.

    :params:

    product_id - holds the integer value for the id of the product to be
    deleted.

    :returns:

    A success message after the product has been deleted.
    """
    username = get_jwt_identity()
    user = Product.query('users', 'username', username)

    if user[-1] is False:
        return jsonify({
            'message': 'You are not authorized to access this!'
        }), 503
    try:
        product_id = int(product_id)
        if not Product.query_all('products'):
            return jsonify({
                'message': 'There are no products for you to delete!'
            }), 400
        elif not Product.query('products', 'product_id', product_id):
            return jsonify({
                'message': 'This product does not exist!'
            }), 400
        db.delete('products', 'product_id', product_id)
        return jsonify({
            'message': 'Product deleted!'
        }), 200
    except ValueError:
        return jsonify({
            'message': 'The product id should be a number!'
        }), 400
