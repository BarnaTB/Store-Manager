import datetime
import re
from passlib.hash import pbkdf2_sha256 as sha256
from database.db import DatabaseConnection

db = DatabaseConnection()


class User:
    """Class handles user object operations"""

    def __init__(self, *args):
        self.username = args[0]
        self.email = args[1]
        self.password = args[2]

    def generate_hash(self):
        """Method to generate a hashed password"""
        return sha256.hash(self.password)

    @staticmethod
    def query_username(username):
        """Method to retrieve a username from the database"""
        user = db.query_username(username)

        if user is None:
            return False
        else:
            return user

    @staticmethod
    def query_email(email):
        """Method to retrieve an email from the database"""
        email = db.query_email(email)

        if email is None:
            return False
        else:
            return True


class Product:
    """Class handles all operations on a product object"""
    products = []

    def __init__(self, *args):
        self.name = args[0]
        self.unit_price = args[1]
        self.quantity = args[2]
        self._id = args[3]


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
