import unittest
from api import app
from flask import json
from api.models import Product
from database.db import DatabaseConnection
from base_test import BaseTest


class TestProduct(BaseTest):
    def setUp(self):
        self.tester = app.test_client(self)
        self.db = DatabaseConnection()

    def test_add_product_not_admin(self):
        """Test non-admin users cannot access add a product"""
        reply = self.login_attendant()
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

        self.assertEqual(reply['message'],
                         'You are not authorized to access this!')
        self.assertEqual(response.status_code, 503)

    def test_admin_add_product(self):
        """Test that admin user can add a product"""
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

        self.assertEqual(reply['message'], 'Product added successfully!')
        self.assertEqual(response.status_code, 201)

    def test_admin_add_product_with_punctutations(self):
        """Test that a user cannot add a product with only punctuation marks"""
        reply = self.login_user()
        token = reply['token']

        product = dict(
            category=';',
            name='sugar',
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

        self.assertEqual(reply['message'], 'One of the required fields is empty or \
contains invalid characters!')
        self.assertEqual(response.status_code, 400)

    def test_add_product_missing_fields(self):
        """Test that empty fields are not accepted"""
        reply = self.login_user()
        token = reply['token']

        product = dict(
            category='groceries',
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
                         'One of the required fields is empty or \
contains invalid characters!')
        self.assertEqual(response.status_code, 400)

    def test_unit_price_must_be_number(self):
        """Test that a unit price is strictly a number"""
        reply = self.login_user()
        token = reply['token']

        product = dict(
            category='groceries',
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
        reply = self.login_user()
        token = reply['token']

        reply = self.add_product()

        self.assertEqual(reply['message'], 'Product added successfully!')

        response = self.tester.get(
            '/api/v1/products',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['products'], Product.products)
        self.assertEqual(response.status_code, 200)

    def test_view_products_from_empty_list(self):
        """Test that a user cannot view products from an empty list"""
        reply = self.login_user()
        token = reply['token']

        response = self.tester.get(
            '/api/v1/products',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'There are not products yet!')
        self.assertEqual(response.status_code, 400)

    def test_view_one_product(self):
        """Test that user can view a single product"""
        reply = self.login_user()
        token = reply['token']

        reply = self.add_product()

        self.assertEqual(reply['message'], 'Product added successfully!')

        response = self.tester.get(
            '/api/v1/products/1',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'Product fetched!')
        self.assertEqual(response.status_code, 200)

    def test_view_product_which_does_exist(self):
        """Test that a user cannot view an object which does not exist"""
        reply = self.login_user()
        token = reply['token']

        reply = self.add_product()

        response = self.tester.get(
            '/api/v1/products/2',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'This product does not exist!')
        self.assertEqual(response.status_code, 400)

    def test_view_one_product_with_vague_id(self):
        """Test that a user cannot view one product with non-integer id"""
        reply = self.login_user()
        token = reply['token']

        reply = self.add_product()

        self.assertEqual(reply['message'], 'Product added successfully!')

        response = self.tester.get(
            '/api/v1/products/2the',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'],
                         'The product id should be a number!')
        self.assertEqual(response.status_code, 400)

    def test_view_single_product_from_empty_list(self):
        """Test that a user cannot view a product from an empty list"""
        reply = self.login_attendant()

        self.assertEqual(reply['message'], 'Logged in!')

        token = reply['token']

        response = self.tester.get(
            '/api/v1/products/1',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'There are no products yet!')
        self.assertEqual(response.status_code, 404)

    def test_update_product(self):
        """Test that a product can be updated successfully"""
        reply = self.login_user()
        token = reply['token']

        reply = self.add_product()

        self.assertEqual(reply['message'], 'Product added successfully!')

        new_product = dict(
            category='groceries',
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

    def test_update_product_id_with_vague_ids(self):
        """Test that a user cannot update a product with non-integer ids"""
        reply = self.login_user()
        token = reply['token']

        reply = self.add_product()

        self.assertEqual(reply['message'], 'Product added successfully!')

        new_product = dict(
            category='groceries',
            name='sukaali',
            quantity='ten',
            unit_price='onethousand'
        )

        response = self.tester.put(
            '/api/v1/products/one',
            content_type='application/json',
            data=json.dumps(new_product),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(
            reply['message'],
            'Product id, quantity and unit price should be numbers!')
        self.assertEqual(response.status_code, 400)

    def test_update_product_with_empty_fields(self):
        """Test admin cannot update product with empty spaces"""
        reply = self.login_user()
        token = reply['token']

        reply = self.add_product()

        self.assertEqual(reply['message'], 'Product added successfully!')

        new_product = dict(
            category='groceries',
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
                         'One of the required fields is empty or \
contains invalid characters!')
        self.assertEqual(response.status_code, 400)

    def test_update_with_words_for_quantity(self):
        """Test user cannot update quantity with words"""
        reply = self.login_user()
        token = reply['token']

        reply = self.add_product()

        self.assertEqual(reply['message'], 'Product added successfully!')

        new_product = dict(
            category='groceries',
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
                         'Product id, quantity and unit price should be \
numbers!')
        self.assertEqual(response.status_code, 400)

    def test_update_product_which_does_not_exist(self):
        """Test that admin cannot a product which does not exist"""
        reply = self.login_user()
        token = reply['token']

        reply = self.add_product()

        self.assertEqual(reply['message'], 'Product added successfully!')

        new_product = dict(
            category='groceries',
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
        reply = self.login_attendant()
        token = reply['token']

        product = dict(
            category='groceries',
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

    def test_admin_delete_product(self):
        """Test admin can delete a product"""
        reply = self.login_user()
        token = reply['token']

        reply = self.add_product()

        self.assertEqual(reply['message'], 'Product added successfully!')

        response = self.tester.delete(
            '/api/v1/products/1',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'Product deleted!')
        self.assertEqual(response.status_code, 200)

    def test_delete_product_attendant(self):
        """Test attendant should not be able to delete a product"""
        reply = self.login_attendant()
        token = reply['token']

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
        reply = self.login_user()
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
        reply = self.login_user()
        token = reply['token']

        reply = self.add_product()

        self.assertEqual(reply['message'], 'Product added successfully!')

        response = self.tester.delete(
            '/api/v1/products/2',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'This product does not exist!')
        self.assertEqual(response.status_code, 400)

    def test_delete_product_with_vague_id(self):
        """Test that user cannot delete a product with non-integer id"""
        reply = self.login_user()
        token = reply['token']

        reply = self.add_product()

        self.assertEqual(reply['message'], 'Product added successfully!')

        response = self.tester.delete(
            '/api/v1/products/the',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'],
                         'The product id should be a number!')
        self.assertEqual(response.status_code, 400)

    def tearDown(self):
        self.db.drop_table('products')
        self.db.drop_table('users')
        self.db.drop_table('sales')
