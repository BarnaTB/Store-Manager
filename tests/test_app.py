import unittest
from api import app
from flask import json


class TestBase(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client(self)

    def test_add_product(self):
        """Test add a product successfully"""
        product = dict(
            name='sugar',
            unit_price=1000,
            quantity='100kg'
        )
        response = self.tester.post(
            '/api/v1/products',
            content_type='application/json',
            data=json.dumps(product)
        )

        reply = json.loads(response.data.decode())

        self.assertIn('Product added successfully!', reply['message'])

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

    def test_unit_price_must_be_number(self):
        """Test that a unit price is strictly a number"""
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

        self.assertIn('The unit price must be a number!', reply['message'])
