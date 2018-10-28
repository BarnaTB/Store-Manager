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

    def test_view_products(self):
        """Test that a user can view all products in the store"""
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

        response = self.tester.get(
            '/api/v1/products'
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['products'], Product.products)
        self.assertEqual(response.status_code, 200)

    def test_view_products_from_empty_list(self):
        """Test that a user cannot view products from an empty list"""
        response = self.tester.get(
            '/api/v1/products'
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'There are not products yet!')
        self.assertEqual(response.status_code, 400)

    def test_view_one_product(self):
        """Test that user can view a single product"""
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

        response = self.tester.get(
            '/api/v1/products/1'
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'Product fetched!')
        self.assertEqual(response.status_code, 200)

    def test_view_product_which_does_exist(self):
        """Test that a user cannot view an object which does not exist"""
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

        response = self.tester.get(
            '/api/v1/products/2'
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'This product does not exist!')
        self.assertEqual(response.status_code, 400)

    def test_view_single_product_from_empty_list(self):
        """Test that a user cannot view a product from an empty list"""
        response = self.tester.get(
            '/api/v1/products/1'
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'There are no products yet!')
        self.assertEqual(response.status_code, 404)

    def test_update_product(self):
        """Test that a product can be updated successfully"""
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

        new_product = dict(
            name='sukaali',
            quantity=100,
            unit_price=1300
        )

        response = self.tester.put(
            '/api/v1/products/1',
            content_type='application/json',
            data=json.dumps(new_product),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'Product updated!')
        self.assertEqual(response.status_code, 201)

    def test_update_product_with_empty_fields(self):
        """Test admin cannot update product with empty spaces"""
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

        new_product = dict(
            name='',
            quantity=100,
            unit_price=1300
        )

        response = self.tester.put(
            '/api/v1/products/1',
            content_type='application/json',
            data=json.dumps(new_product),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'],
                         'One of the required fields is empty!')
        self.assertEqual(response.status_code, 400)

    def test_update_with_words_for_quantity(self):
        """Test user cannot update quantity with words"""
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

        new_product = dict(
            name='sukaali',
            quantity='kilo kikumi',
            unit_price=1300
        )

        response = self.tester.put(
            '/api/v1/products/1',
            content_type='application/json',
            data=json.dumps(new_product),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'],
                         'The unit price and quantity must be numbers!')
        self.assertEqual(response.status_code, 400)

    def test_update_product_which_does_not_exist(self):
        """Test that admin cannot a product which does not exist"""
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

        new_product = dict(
            name='sukaali',
            quantity=100,
            unit_price=1300
        )

        response = self.tester.put(
            '/api/v1/products/2',
            content_type='application/json',
            data=json.dumps(new_product),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'This product does not exist!')
        self.assertEqual(response.status_code, 400)

    def test_user_update_product_unauthorized(self):
        """Test attendant cannot update product"""
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
        response = self.tester.put(
            '/api/v1/products/1',
            content_type='application/json',
            data=json.dumps(product),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'],
                         'You are not authorized to access this!')
        self.assertEqual(response.status_code, 503)

    def tearDown(self):
        self.db.drop_table('products')
        self.db.drop_table('users')
        self.db.drop_table('sales')
