import unittest
import json
from api import app
from database.db import DatabaseConnection
from base_test import BaseTest


class TestAuth(BaseTest):
    """Class tests registeration and login views"""

    def setUp(self):
        self.tester = app.test_client(self)
        self.db = DatabaseConnection()
        self.base = BaseTest()

    def test_successful_registration(self):
        """Test that a user can register successfully"""
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

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'barna successfully registered!')
        self.assertEqual(response.status_code, 201)

    def test_registration_with_empty_username_field(self):
        """Test that a user cannot register with empty fields"""
        reply = self.login_user()
        token = reply['token']

        user = dict(
            username='',
            email='barna@mail.com',
            password='Pass1234'
        )

        response = self.tester.post(
            '/api/v1/signup',
            content_type='application/json',
            data=json.dumps(user),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'],
                         'Username cannot be empty or contain numbers!')
        self.assertEqual(response.status_code, 400)

    def test_registration_with_empty_email_field(self):
        """Test that a user cannot register with empty fields"""
        reply = self.login_user()
        token = reply['token']

        user = dict(
            username='barna',
            email='',
            password='Pass1234'
        )

        response = self.tester.post(
            '/api/v1/signup',
            content_type='application/json',
            data=json.dumps(user),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'],
                         'Email cannot be empty and must be in the form \
(john.doe@example.com)')
        self.assertEqual(response.status_code, 400)

    def test_registration_with_empty_password_field(self):
        """Test that a user cannot register with empty fields"""
        reply = self.login_user()
        token = reply['token']

        user = dict(
            username='barna',
            email='barna@mail.com',
            password=''
        )

        response = self.tester.post(
            '/api/v1/signup',
            content_type='application/json',
            data=json.dumps(user),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'],
                         'Password should contain at least one uppercase, \
lowercase and number characcters and must be longer than 5 characters!')
        self.assertEqual(response.status_code, 400)

    def test_user_registration_with_registered_username(self):
        """Test that a user cannot register with a registered username"""
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

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'barna successfully registered!')
        self.assertEqual(response.status_code, 201)

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

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'This username is already taken!')
        self.assertEqual(response.status_code, 400)

    def test_registration_with_registered_email(self):
        """Test that a user cannot register with a registered email"""
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

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'barna successfully registered!')
        self.assertEqual(response.status_code, 201)

        user = dict(
            username='barnabas',
            email='barna@mail.com',
            password='Pass1234'
        )

        response = self.tester.post(
            '/api/v1/signup',
            content_type='application/json',
            data=json.dumps(user),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'This email is already taken!')
        self.assertEqual(response.status_code, 400)

    def test_user_login(self):
        """Test that a user can login successfully"""
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

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'barna successfully registered!')
        self.assertEqual(response.status_code, 201)

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

        self.assertEqual(reply['message'], 'Logged in!')
        self.assertEqual(response.status_code, 200)

    def test_login_with_empty_input_fields(self):
        """Test that a user cannot login with empty inputs"""
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

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'barna successfully registered!')
        self.assertEqual(response.status_code, 201)

        user = dict(
            username='',
            password=''
        )

        response = self.tester.post(
            '/api/v1/login',
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'],
                         'One of the required fields is empty!')
        self.assertEqual(response.status_code, 400)

    def test_login_with_wrong_username(self):
        """Test that a user cannot login with a wrong username"""
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

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'barna successfully registered!')
        self.assertEqual(response.status_code, 201)

        user = dict(
            username='barn',
            password='Pass1234'
        )

        response = self.tester.post(
            '/api/v1/login',
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'Sorry wrong username!')
        self.assertEqual(response.status_code, 400)

    def test_login_with_wrong_password(self):
        """Test that a user cannot login with a wrong password"""
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

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'barna successfully registered!')
        self.assertEqual(response.status_code, 201)

        user = dict(
            username='barna',
            password='Pass234'
        )

        response = self.tester.post(
            '/api/v1/login',
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'Sorry wrong password!')
        self.assertEqual(response.status_code, 400)

    def tearDown(self):
        self.db.drop_table('users')
