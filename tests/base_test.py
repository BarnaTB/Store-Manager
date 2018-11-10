import json
import unittest
from api import app
from database.db import DatabaseConnection


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client(self)
        self.db = DatabaseConnection()

    def login_user(self):
        """Base method for logging in a user"""
        user = dict(
            username='admin',
            password='Pass1234'
        )

        response = self.tester.post(
            '/api/v1/login',
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())

        return reply

    def add_product(self):
        """Base method to add a product to the store"""
        reply = self.login_user()
        token = reply['token']

        product = dict(
            category='groceries',
            name='Sugar',
            unit_price=1000,
            quantity=100
        )
        response = self.tester.post(
            '/api/v1/products',
            content_type='application/json',
            data=json.dumps(product),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        reply = json.loads(response.data.decode())

        return reply

    def login_attendant(self):
        """Base method to register and login an attendant"""
        reply = self.login_user()
        token = reply['token']

        user = dict(
            username='barna',
            email='barna@mail.com',
            password='Pass1234'
        )

        response = self.tester.post(
            '/api/v1/signup',
            content_type='application/json',
            data=json.dumps(user),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        user = dict(
            username='barna',
            password='Pass1234'
        )

        response = self.tester.post(
            '/api/v1/login',
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())

        return reply
