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
