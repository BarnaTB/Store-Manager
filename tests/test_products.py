import unittest
from api import app
from flask import json
from api.models import Product


class TestProduct(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client(self)

    def test_add_product(self):
        """Test add a product successfully"""
        product = dict(
            name='Sugar',
            unit_price=1000,
            quantity=100
        )
        response = self.tester.post(
            '/api/v1/products',
            content_type='application/json',
            data=json.dumps(product)
        )

        reply = json.loads(response.data.decode())

        self.assertIn('Product added successfully!', reply['message'])
        self.assertEqual(response.status_code, 201)

    def test_add_product_missing_fields(self):
        """Test that empty fields are not accepted"""
        product = dict(
            name='',
            unit_price='',
            quantity=''
        )
        response = self.tester.post(
            '/api/v1/products',
            content_type='application/json',
            data=json.dumps(product)
        )
        reply = json.loads(response.data.decode())

        self.assertIn('One of the required fields is empty!', reply['message'])
        self.assertEqual(response.status_code, 400)

    def test_unit_price_must_be_number(self):
        """Test that a unit price and quantity are strictly numbers"""
        product = dict(
            name='Sugar',
            unit_price='bitaano',
            quantity='100kgs'
        )
        response = self.tester.post(
            '/api/v1/products',
            content_type='application/json',
            data=json.dumps(product)
        )
        reply = json.loads(response.data.decode())

        self.assertIn('The unit price and quantity must be numbers!', reply['message'])
        self.assertEqual(response.status_code, 400)

    def test_view_products(self):
        """Test that a user can view all products in the store"""
        product = dict(
            name='Sugar',
            unit_price=1000,
            quantity=100
        )
        response = self.tester.post(
            '/api/v1/products',
            content_type='application/json',
            data=json.dumps(product)
        )

        reply = json.loads(response.data.decode())

        self.assertIn('Product added successfully!', reply['message'])
        self.assertEqual(response.status_code, 201)
        response = self.tester.get(
            '/api/v1/products'
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['products'], [
                         product.__dict__ for product in Product.products])
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
        product = dict(
            name='Sugar',
            unit_price=1000,
            quantity=100
        )
        response = self.tester.post(
            '/api/v1/products',
            content_type='application/json',
            data=json.dumps(product)
        )

        reply = json.loads(response.data.decode())

        self.assertIn('Product added successfully!', reply['message'])
        self.assertEqual(response.status_code, 201)

        response = self.tester.get(
            '/api/v1/products/1'
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'Product fetched!')
        self.assertEqual(response.status_code, 200)

    def test_view_product_which_does_exist(self):
        """Test that a user cannot view an object which does not exist"""
        product = dict(
            name='Sugar',
            unit_price=1000,
            quantity=100
        )
        response = self.tester.post(
            '/api/v1/products',
            content_type='application/json',
            data=json.dumps(product)
        )

        reply = json.loads(response.data.decode())

        self.assertIn('Product added successfully!', reply['message'])
        self.assertEqual(response.status_code, 201)

        response = self.tester.get(
            '/api/v1/products/2'
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'This product does not exist!')
        self.assertEqual(response.status_code, 404)

    def test_view_single_product_from_empty_list(self):
        """Test that a user cannot view a product from an empty list"""
        response = self.tester.get(
            '/api/v1/products/1'
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'There are no products yet!')
        self.assertEqual(response.status_code, 404)

    def tearDown(self):
        Product.products.clear()
