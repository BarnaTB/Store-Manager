import datetime
import re
from passlib.hash import pbkdf2_sha256 as sha256
from database.db import DatabaseConnection

db = DatabaseConnection()


class Product(object):
    """Class handles all operations on a product object"""
    products = []

    def __init__(self, name, quantity, unit_price):
        self.name = name
        self.quantity = quantity
        self.unit_price = unit_price

    def insert_product(self):
        """
        Method enables user to add a product to the database

        :returns:

        False - if that product is already in the database.

        A dictionary object of the product that has been added.
        """
        if db.query('products', 'name', self.name) is not None:
            return False
        db.insert_product(self.name, self.quantity, self.unit_price)
        product = db.query('products', 'name', self.name)
        return {
            '_id': product[0],
            'name': product[1],
            'quantity': product[2],
            'unit_price': product[3]
        }

    @staticmethod
    def query_all(table):
        """
        Method enables to retrieve all items from the list

        :returns:

        False - if there are no products in the database yet.

        A list of all products in the database.
        """

        products = db.query_all(table)
        if products == []:
            return False
        else:
            Product.products.clear()
            for product in products:
                product_dict = {
                    '_id': product[0],
                    'name': product[1],
                    'unit_price': product[2],
                    'quantity': product[3]
                }
                Product.products.append(product_dict)
            return Product.products

    @staticmethod
    def query(table, column, value):
        """
        Method enables user to retrieve a specific item

        :params:

        table - holds the name of the table to be queried.

        column - holds the name of the column from which
        the value is to be queried.

        value - holds the value which is to be queried from the table

        :returns:

        False - if the product being queried does not exist.

        A dictionary object of the product that has been fetched.
        """

        product = db.query(table, column, value)
        if product == [] or product is None:
            return False
        return product

    @staticmethod
    def update(*args):
        """
        Method enables user to update a specific record in the database

        :params:

        table - takes in the name of the table with that record.

        column - takes in the name of the column to be updated.

        new_status - takes in the new value of the cell.

        cell - takes in the name of the conditional cell.

        value - takes in the value of the condition for the cell to be updated.
        """
        table = args[0]
        column = args[1]
        new_status = args[2]
        cell = args[3]
        value = args[4]

        db.update(table, column, new_status, cell, value)


class Sale(Product):
    """Class handles all operations of a sale."""
    sales = []

    def __init__(self, name, quantity, unit_price, author, total=0, date=''):
        Product.__init__(self, name, quantity, unit_price)
        self.author = author
        self.total = total
        self.date = date

    def insert_sale(self):
        """
        Method enables user make a sales record.

        :returns:

        a dictionary object of the sales record.
        """
        db.insert_sale(self.author, self.name, self.quantity,
                       self.unit_price, self.total, self.date)
        sale = db.query('sales', 'purchase_date', self.date)

        return {
            'sale_id': sale[0],
            'attendant': sale[1],
            'name': sale[2],
            'quantity': sale[3],
            'unit_price': sale[4],
            'total': sale[5],
            'date': sale[6]
        }

    @staticmethod
    def query_all_sales(table):
        """
        Method enables to retrieve all items from the list

        :returns:

        False - if there are no products in the database yet.

        A list of all products in the database.
        """

        sales = db.query_all(table)
        if sales == []:
            return False
        else:
            Sale.sales.clear()
            for sale in sales:
                sales_dict = {
                    '_id': sale[0],
                    'attendant': sale[1],
                    'name': sale[2],
                    'quantity': sale[3],
                    'unit_price': sale[4],
                    'total': sale[5],
                    'purchase_date': sale[6]
                }
                Sale.sales.append(sales_dict)
            return Sale.sales


class User:
    """Class handles user object operations"""

    def __init__(self, username, email, password, admin='false'):
        self.username = username
        self.email = email
        self.password = password
        self.admin = admin

    def generate_hash(self):
        """Method to generate a hashed password"""
        return sha256.hash(self.password)

    @staticmethod
    def verify_password(username, password):
        """Method to verify a password hash"""
        user = User.query_username(username)
        if not sha256.verify(password, user[3]):
            return False
        return True

    def insert_user(self):
        """Method to add a user into the database"""
        db.insert_user(self.username, self.email, self.password, self.admin)

        return self.username
