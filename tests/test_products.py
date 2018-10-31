import unittest
from api import app
from flask import json
from api.models import Product
from database.db import DatabaseConnection


class TestProduct(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client(self)
        self.db = DatabaseConnection()

    def test_add_product_not_admin(self):
        """Test non-admin users cannot access add a product"""
        user = dict(
            username='barna',
            email='barna@mail.com',
            password='Pass1234'
        )

        response = self.tester.post(
            '/api/v1/signup',
            content_type='application/json',
            data=json.dumps(user)
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
        token = reply['token']

        product = dict(
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

        self.assertEqual(reply['message'],
                         'You are not authorized to access this!')
        self.assertEqual(response.status_code, 503)

    def test_admin_add_product(self):
        """Test that admin user can add a product"""
        user = dict(
            username='admin',
            email='admin@store.com',
            password='Pass1234'
        )

        response = self.tester.post(
            '/api/v1/signup',
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'admin successfully registered!')
        self.assertEqual(response.status_code, 201)

        self.db.update('users', 'admin', 'true', 'username', 'admin')

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

        self.assertEqual(reply['message'], 'Logged in!')
        self.assertEqual(response.status_code, 200)
        token = reply['token']

        product = dict(
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

        self.assertEqual(reply['message'], 'Product added successfully!')
        self.assertEqual(response.status_code, 201)

    def test_add_product_missing_fields(self):
        """Test that empty fields are not accepted"""
        user = dict(
            username='admin',
            email='admin@store.com',
            password='Pass1234'
        )

        response = self.tester.post(
            '/api/v1/signup',
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'admin successfully registered!')
        self.assertEqual(response.status_code, 201)

        self.db.update('users', 'admin', 'true', 'username', 'admin')

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

        self.assertEqual(reply['message'], 'Logged in!')
        self.assertEqual(response.status_code, 200)
        token = reply['token']

        product = dict(
            name='',
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

        self.assertEqual(reply['message'],
                         'One of the required fields is empty!')
        self.assertEqual(response.status_code, 400)

    def test_unit_price_must_be_number(self):
        """Test that a unit price is strictly a number"""
        user = dict(
            username='admin',
            email='admin@store.com',
            password='Pass1234'
        )

        response = self.tester.post(
            '/api/v1/signup',
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'admin successfully registered!')
        self.assertEqual(response.status_code, 201)

        self.db.update('users', 'admin', 'true', 'username', 'admin')

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

        self.assertEqual(reply['message'], 'Logged in!')
        self.assertEqual(response.status_code, 200)
        token = reply['token']

        product = dict(
            name='sugar',
            unit_price='enamba',
            quantity=100
        )
        response = self.tester.post(
            '/api/v1/products',
            content_type='application/json',
            data=json.dumps(product),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'],
                         'The unit price and quantity must be numbers!')
        self.assertEqual(response.status_code, 400)

    def test_product_already_exists(self):
        """Test that a user cannot add a product which already exists"""
        user = dict(
            username='admin',
            email='admin@store.com',
            password='Pass1234'
        )

        response = self.tester.post(
            '/api/v1/signup',
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'admin successfully registered!')
        self.assertEqual(response.status_code, 201)

        self.db.update('users', 'admin', 'true', 'username', 'admin')

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

        self.assertEqual(reply['message'], 'Logged in!')
        self.assertEqual(response.status_code, 200)
        token = reply['token']

        product = dict(
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

        self.assertEqual(reply['message'], 'Product added successfully!')
        self.assertEqual(response.status_code, 201)

        response = self.tester.post(
            '/api/v1/products',
            content_type='application/json',
            data=json.dumps(product),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'This product already exists!')
        self.assertEqual(response.status_code, 400)

    def test_admin_delete_product(self):
        """Test admin can delete a product"""
        user = dict(
            username='admin',
            email='admin@store.com',
            password='Pass1234'
        )

        response = self.tester.post(
            '/api/v1/signup',
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'admin successfully registered!')
        self.assertEqual(response.status_code, 201)

        self.db.update('users', 'admin', 'true', 'username', 'admin')

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

        self.assertEqual(reply['message'], 'Logged in!')
        self.assertEqual(response.status_code, 200)
        token = reply['token']

        product = dict(
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

        self.assertEqual(reply['message'], 'Product added successfully!')
        self.assertEqual(response.status_code, 201)

        response = self.tester.delete(
            '/api/v1/products/1',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'Product deleted!')
        self.assertEqual(response.status_code, 200)

    def test_delete_product_attendant(self):
        """Test attendant should not be able to delete a product"""
        user = dict(
            username='barna',
            email='barna@mail.com',
            password='Pass1234'
        )

        response = self.tester.post(
            '/api/v1/signup',
            content_type='application/json',
            data=json.dumps(user)
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
        token = reply['token']

        product = dict(
            name='Sugar',
            unit_price=1000,
            quantity=100
        )
        response = self.tester.delete(
            '/api/v1/products/1',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'],
                         'You are not authorized to access this!')
        self.assertEqual(response.status_code, 503)

    def test_delete_product_without_products(self):
        """Test that a user cannot delete a product if there aren't any"""
        user = dict(
            username='admin',
            email='admin@store.com',
            password='Pass1234'
        )

        response = self.tester.post(
            '/api/v1/signup',
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'admin successfully registered!')
        self.assertEqual(response.status_code, 201)

        self.db.update('users', 'admin', 'true', 'username', 'admin')

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

        self.assertEqual(reply['message'], 'Logged in!')
        self.assertEqual(response.status_code, 200)
        token = reply['token']

        response = self.tester.delete(
            '/api/v1/products/1',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'],
                         'There are no products for you to delete!')
        self.assertEqual(response.status_code, 400)

    def test_delete_product_which_does_not_exist(self):
        """Test that user cannot delete a product which does not exist"""
        user = dict(
            username='admin',
            email='admin@store.com',
            password='Pass1234'
        )

        response = self.tester.post(
            '/api/v1/signup',
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'admin successfully registered!')
        self.assertEqual(response.status_code, 201)

        self.db.update('users', 'admin', 'true', 'username', 'admin')

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

        self.assertEqual(reply['message'], 'Logged in!')
        self.assertEqual(response.status_code, 200)
        token = reply['token']

        product = dict(
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

        self.assertEqual(reply['message'], 'Product added successfully!')
        self.assertEqual(response.status_code, 201)

        response = self.tester.delete(
            '/api/v1/products/2',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'This product does not exist!')
        self.assertEqual(response.status_code, 400)

    def test_delete_product_with_vague_id(self):
        """Test that user cannot delete a product with non-integer id"""
        user = dict(
            username='admin',
            email='admin@store.com',
            password='Pass1234'
        )

        response = self.tester.post(
            '/api/v1/signup',
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'admin successfully registered!')
        self.assertEqual(response.status_code, 201)

        self.db.update('users', 'admin', 'true', 'username', 'admin')

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

        self.assertEqual(reply['message'], 'Logged in!')
        self.assertEqual(response.status_code, 200)
        token = reply['token']

        product = dict(
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

        self.assertEqual(reply['message'], 'Product added successfully!')
        self.assertEqual(response.status_code, 201)

        response = self.tester.delete(
            '/api/v1/products/the',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'The product id should be a number!')
        self.assertEqual(response.status_code, 400)

    def tearDown(self):
        self.db.drop_table('products')
        self.db.drop_table('users')
        self.db.drop_table('sales')
