from flask import request, jsonify, Blueprint, json
from api.models import Product, Sale, User
from api.validator import ValidateProduct, ValidateSale, ValidateUser
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


@blueprint.route('/products', methods=['GET'])
def view_products():
    """
    Function enables store owner or attendant to view all products in the
    store.

    :returns:

    A list of products from the store.
    """
    if not Product.query_all('products'):
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
    if not Product.query_all('products'):
        return jsonify({
            'message': 'There are no products yet!'
        }), 404
    product = Product.query('products', 'product_id', product_id)
    if not product:
        return jsonify({
            'message': 'This product does not exist!'
        }), 400
    product_dict = {
            '_id': product[0],
            'name': product[1],
            'quantity': product[2],
            'unit_price': product[3]
        }
    return jsonify({
        'product': product_dict,
        'message': 'Product fetched!'
    }), 200


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
    product_dict = {
            '_id': product[0],
            'name': product[1],
            'quantity': product[2],
            'unit_price': product[3]
        }
    if product_dict['quantity'] <= 0:
        return jsonify({
            'message': 'Product is out of stock!'
        }), 400
    elif product_dict['quantity'] < quantity:
        return jsonify({
            'message': 'Unfortunately we have less than you require!'
        }), 400
    unit_price = product_dict['unit_price']
    total = unit_price * quantity
    now = datetime.datetime.now()
    a_sale = Sale(name, quantity, unit_price, username, total,
                  now.strftime('%H:%M:%S on %a, %dth %B %Y'))
    sale = a_sale.insert_sale()
    new_quantity = product_dict['quantity'] - quantity
    a_sale.update('products', 'quantity', new_quantity, 'name', name)
    return jsonify({
        'sale': sale,
        'message': 'Sold!'
    }), 201


@blueprint.route('/sales', methods=['GET'])
@jwt_required
def view_all_sales():
    """
    Function enables store owner to view all sales records.

    :returns:

    A list of all sales made by all store attendants.
    """
    username = get_jwt_identity()
    user = User.query_username(username)

    if user[-1] is False:
        return jsonify({
            'message': 'You are not authorized to access this!'
        }), 503
    elif not Sale.query_all_sales('sales'):
        return jsonify({
            'message': 'No sales yet!'
        }), 400
    return jsonify({
        'sales': Sale.query_all_sales('sales'),
        'message': 'Sales fetched successfully!'
    }), 200


@blueprint.route('/sales/<int:sale_id>', methods=['GET'])
@jwt_required
def view_single_sale(sale_id):
    """
    Function enables store owner and attendant to be able to view a single
    sales record.

    :params:

    sale_id - holds integer value of the id of the individual sale to be viewed

    :returns:

    Details of the sale whose id matches the one entered by the user.
    """
    username = get_jwt_identity()

    sale = Sale.query('sales', 'sales_id', sale_id)

    if not Sale.query_all('sales'):
        return jsonify({
            'message': 'No sales yet!'
        }), 400
    elif not sale:
        return jsonify({
            'message': 'This sale does not exist!'
        }), 400
    sale_dict = {
        'sales_id': sale[0],
        'sale_author': sale[1],
        'name': sale[2],
        'quantity': sale[3],
        'unit_price': sale[4],
        'total_price': sale[5],
        'purchase_date': sale[6]
    }
    user = User.query_username(username)

    if sale_dict['sale_author'] != username and user[-1] is False:
        return jsonify({
            'message': 'You are not authorized to access this!'
        }), 503
    return jsonify({
        'sale': sale_dict,
        'message': 'Sale fetched!'
    }), 200
