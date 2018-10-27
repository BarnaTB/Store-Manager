from flask import request, jsonify, Blueprint, json
from api.models import Product, Sale, User
from api.validator import ValidateItem, ValidateUser
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
    elif User.query_username(username):
        return jsonify({
            'message': 'This username is already taken!'
        }), 400
    elif User.query_email(email):
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
    elif not User.query_username(username):
        return jsonify({
            'message': 'Sorry wrong username!'
        }), 400
    elif not User.verify_password(username, password):
        return jsonify({
            'message': 'Sorry wrong password!'
        }), 400
    user = User.query_username(username)
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
    user = User.query_username(username)

    if user[-1] is False:
        return jsonify({
            'message': 'You are not authorized to access this!'
        }), 503
    else:
        data = request.get_json()

        name = data.get('name')
        unit_price = data.get('unit_price')
        quantity = data.get('quantity')
        _id = len(Product.products) + 1

        validate_product = ValidateItem(name, unit_price, quantity, _id)
        product = Product(name, quantity, unit_price, _id)
        if validate_product.validate() is False:
            return jsonify({
                'message': 'One of the required fields is empty!'
            }), 400
        elif not isinstance(unit_price, int) or not isinstance(quantity, int):
            return jsonify({
                'message': 'The unit price and quantity must be numbers!'
            }), 400
        elif not product.insert_product():
            return jsonify({
                'message': 'This product already exists!'
            }), 400
        return jsonify({
            'product': product.__dict__,
            'message': 'Product added successfully!'
        }), 201


@blueprint.route('/products', methods=['GET'])
def view_products():
    """
    Function enables store owner or attendant to view all products in the
    store.

    :returns:

    A list of products from the store.
    """
    if not Product.query_all_products():
        return jsonify({
            'message': 'There are not products yet!'
        }), 400
    return jsonify({
        'products': Product.products
    }), 200


@blueprint.route('/products/<int:product_id>')
def view_single_product(product_id):
    """
    Function enables store owner or attendant view details of a specific
    product in the store.

    :params:

    product_id - holds integer value of the id of the product which is to be
    viewed.

    :returns:

    A product that matches the product_id that was entered.
    """
    if not Product.query_all_products():
        return jsonify({
            'message': 'There are no products yet!'
        }), 404
    product = Product.query_product(product_id)
    if not product:
        return jsonify({
            'message': 'This product does not exist!'
        }), 400
    return jsonify({
        'product': product,
        'message': 'Product fetched!'
    }), 200


@blueprint.route('/sales', methods=['POST'])
def add_sale():
    """
    Function enables store attendant to create a sale.

    :returns:

    The sales records which was just created.
    """
    data = request.get_json()

    name = data.get('name')
    unit_price = data.get('unit_price')
    quantity = data.get('quantity')
    _id = len(Sale.sales) + 1

    sale = ValidateItem(name, unit_price, quantity, _id)

    if not sale.validate():
        return jsonify({
            'message': 'One of the required fields is empty!'
        }), 400
    elif not isinstance(unit_price, int) or not isinstance(quantity, int):
        return jsonify({
            'message': 'Quantity and unit price should be numbers!'
        }), 400
    total = unit_price * quantity
    now = datetime.datetime.now()
    a_sale = Sale(_id, name, unit_price, quantity, total=total,
                  date=now.strftime('%H:%M:%S on %a, %dth %B %Y'))
    Sale.sales.append(a_sale.__dict__)
    return jsonify({
        'sale': a_sale.__dict__,
        'message': 'Sold!'
    }), 201


@blueprint.route('/sales', methods=['GET'])
def view_all_sales():
    """
    Function enables store owner to view all sales records.

    :returns:

    A list of all sales made by all store attendants.
    """
    if len(Sale.sales) == 0:
        return jsonify({
            'message': 'No sales yet!'
        }), 400
    return jsonify({
        'sales': Sale.sales,
        'message': 'Sales fetched successfully!'
    })


@blueprint.route('/sales/<int:sale_id>', methods=['GET'])
def view_single_sale(sale_id):
    """
    Function enables store owner and attendant to be able to view a single
    sales record.

    :params:

    sale_id - holds integer value of the id of the individual sale to be viewed

    :returns:

    Details of the sale whose id matches the one entered by the user.
    """
    try:
        if len(Sale.sales) == 0:
            return jsonify({
                'message': 'No sales yet!'
            }), 404
        sale = Sale.sales[sale_id - 1]
        return jsonify({
            'product': sale,
            'message': 'Sale fetched!'
        }), 200
    except IndexError:
        return jsonify({
            'message': 'This sale does not exist!'
        }), 404
