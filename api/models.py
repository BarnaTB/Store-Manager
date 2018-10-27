import datetime
import re
from passlib.hash import pbkdf2_sha256 as sha256
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

    def insert_product(self):
        """Method enables user to add a product to the database"""
        if db.query('products', 'name', self.name) is not None:
            return False
        db.insert_product(self.name, self.unit_price, self.quantity)
        product = db.query('products', 'name', self.name)
        return {
            'name': product[1],
            'unit_price': product[2],
            'quantity': product[3]
        }

    @staticmethod
    def query_all_products():
        """Method enables to retrieve all items from the list"""

        products = db.query_all('products')
        if products == []:
            return False
        else:
            Product.products.clear()
            for product in products:
                product_dict = {
                    'name': product[1],
                    'unit_price': product[2],
                    'quantity': product[3]
                }
                Product.products.append(product_dict)
            return Product.products

    @staticmethod
    def query_product(product_id):
        """Method enables user to retrieve a specific product"""

        product = db.query('products', 'product_id', product_id)
        if product == [] or product is None:
            return False
        return {
            'name': product[1],
            'unit_price': product[2],
            'quantity': product[3]
        }


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
    def query_username(username):
        """Method to retrieve a username from the database"""
        user = db.query('users', 'username', username)

        if user is None:
            return False
        else:
            return user

    @staticmethod
    def query_email(email):
        """Method to retrieve an email from the database"""
        email = db.query('users', 'email', email)

        if email is None:
            return False
        else:
            return True

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
