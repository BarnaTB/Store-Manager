import datetime


class Product:
    """Class handles all operations on a product object"""
    products = [
        {
            'name': 'coffee',
            'unit_price': 1000,
            'quantity': 100,
            '_id': 1
        }
    ]

    def __init__(self, *args):
        self.name = args[0]
        self.unit_price = args[1]
        self.quantity = args[2]
        self._id = args[3]

    def validate_product(self):
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


class Sale:
    """Class handles all operations of a sale."""
    sales = [
        {
            "_id": 1,
            "date": "20:34:34 on Tue, 23th October 2018",
            "item_name": "water",
            "quantity": 100,
            "total": 100000,
            "unit_price": 1000
        }
    ]

    def __init__(self, *args, total=0, date=''):
        self._id = args[0]
        self.item_name = args[1]
        self.unit_price = args[2]
        self.quantity = args[3]
        self.total = total
        self.date = date

    def validate_sale(self):
        """
        Method validates a sale.

        :returns:

        True - if the sale is valid.

        False - if the sale is invalid.
        """
        if self.item_name == '' or not self.unit_price or not self.quantity or\
                self.item_name.isspace():
            return False
        else:
            return True
