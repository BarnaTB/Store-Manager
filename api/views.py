from flask import request, jsonify, Blueprint
from api.models import Product


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

    product = Product(name, unit_price, quantity)

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
        'product': data,
        'message': 'Product added successfully!'
    }), 201
