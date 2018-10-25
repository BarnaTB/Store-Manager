import datetime
from database.db import DatabaseConnection

db = DatabaseConnection()


class Product:
    """Class handles all operations on a product object"""
    products = []

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
                self.name.isspace() or self.quantity.isspace():
            return False
        else:
            return True

    @staticmethod
    def add_product():
        """
        Method adds a product into the database.

        :returns:

        The product that has been added to the database
        """
        db.


class Sale:
    """Class handles all operations of a sale."""
    sales = []

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
