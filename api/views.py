from flask import request, jsonify, Blueprint, json
from api.models import Product, Sale
import datetime


blueprint = Blueprint('application', __name__)


@blueprint.route('/products', methods=['POST'])
def add_product():
    """
    Function adds a product to the products list.

    :returns:

    a success message and the product.
    """
    data = request.get_json()

    name = data.get('name')
    unit_price = data.get('unit_price')
    quantity = data.get('quantity')
    _id = len(Product.products) + 1

    product = Product(name, unit_price, quantity, _id)

    if product.validate_product() is False:
        return jsonify({
            'message': 'One of the required fields is empty!'
        }), 400
    if not isinstance(unit_price, int):
        return jsonify({
            'message': 'The unit price must be a number!'
        }), 400
    Product.products.append(product)
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
    if len(Product.products) == 0:
        return jsonify({
            'message': 'There are not products yet!'
        }), 400
    return jsonify({
        'products': [product.__dict__ for product in Product.products]
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
    try:
        if len(Product.products) == 0:
            return jsonify({
                'message': 'There are no products yet!'
            }), 404
        product = Product.products[product_id - 1]
        return jsonify({
            'product': product.__dict__,
            'message': 'Product fetched!'
        }), 200
    except IndexError:
        return jsonify({
            'message': 'This product does not exist!'
        }), 404


@blueprint.route('/sales', methods=['POST'])
def add_sale():
    """
    Function enables store attendant to create a sale.

    :returns:

    The sales records which was just created.
    """
    data = request.get_json()

    item_name = data.get('item_name')
    unit_price = data.get('unit_price')
    quantity = data.get('quantity')
    _id = len(Sale.sales) + 1

    sale = Sale(_id, item_name, unit_price, quantity)

    if not sale.validate_sale():
        return jsonify({
            'message': 'One of the required fields is empty!'
        }), 400
    if not isinstance(unit_price, int) or not isinstance(quantity, int):
        return jsonify({
            'message': 'Quantity and unit price should be numbers!'
        }), 400
    total = unit_price * quantity
    now = datetime.datetime.now()
    a_sale = Sale(_id, item_name, unit_price, quantity, total=total,
                  date=now.strftime('%H:%M:%S on %a, %dth %B %Y'))
    Sale.sales.append(a_sale.__dict__)
    print(Sale.sales)
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

    Deatils of the sale whose id matches the one entered by the user.
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
