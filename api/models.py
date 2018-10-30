import datetime


class Product(object):
    """Class handles all operations on a product object"""

    products = [
        {
            'name': 'coffee',
            'unit_price': 1000,
            'quantity': 100,
            '_id': 1
        }
    ]

    def __init__(self, name, unit_price, quantity, _id):
        self.name = name
        self.unit_price = unit_price
        self.quantity = quantity
        self._id = _id

    def validate(self):
        """
        Method validates the attributes of a product.

        :returns:

        True - if the product details are all valid.

        False - if one or all of the product details  are invalid.
        """

        if not self.name or not self.unit_price or not self.quantity or\
                self.name.isspace():
            return False
        else:
            return True


class Sale(Product):
    """Class handles all operations of a sale."""

    sales = [
        {
            "_id": 1,
            "date": "20:34:34 on Tue, 23th October 2018",
            "name": "water",
            "quantity": 100,
            "total": 100000,
            "unit_price": 1000
        }
    ]

    def __init__(self, name, unit_price, quantity, _id, total=0, date=''):
        Product.__init__(self, name, unit_price, quantity, _id)
        self.total = total
        self.date = date
