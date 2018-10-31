from flask import request, jsonify, Blueprint, json
from api.models import User, Product, Sale
from api.validator import ValidateUser, ValidateProduct, ValidateSale
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
    else:
        data = request.get_json()

        name = data.get('name')
        quantity = data.get('quantity')
        unit_price = data.get('unit_price')

        validate_product = ValidateProduct(name, quantity, unit_price)
        product = Product(name, quantity, unit_price)
        if validate_product.validate() is False:
            return jsonify({
                'message': 'One of the required fields is empty!'
            }), 400
        elif not isinstance(unit_price, int) or not isinstance(quantity, int):
            return jsonify({
                'message': 'The unit price and quantity must be numbers!'
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


@blueprint.route('/sales', methods=['POST'])
@jwt_required
def add_sale():
    """
    Function enables store attendant to create a sale.
    :returns:
    The sales records which was just created.
    """
    username = get_jwt_identity()

    data = request.get_json()

    name = data.get('name')
    quantity = data.get('quantity')

    sale = ValidateSale(name, quantity)

    if not sale.validate():
        return jsonify({
            'message': 'One of the required fields is empty!'
        }), 400
    elif not isinstance(quantity, int):
        return jsonify({
            'message': 'Quantity should be a number!'
        }), 400
    product = Sale.query('products', 'name', name)
    if not product:
        return jsonify({
            'message': 'This product does not exist!'
        }), 400
    elif product[2] <= 0:
        return jsonify({
            'message': 'Product is out of stock!'
        }), 400
    elif product[2] < quantity:
        return jsonify({
            'message': 'Unfortunately we have less than you require!'
        }), 400
    total = product[3] * quantity
    now = datetime.datetime.now()
    a_sale = Sale(name, quantity, product[3], username, total,
                  now.strftime('%H:%M:%S on %a, %dth %B %Y'))
    sale = a_sale.insert_sale()
    new_quantity = product[2] - quantity
    a_sale.update('products', 'quantity', new_quantity, 'name', name)
    return jsonify({
        'sale': sale,
        'message': 'Sold!'
    }), 201
