import unittest
from api import app
from flask import json


class TestSale(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client(self)

    def test_add_sale(self):
        """Test that a sales can be added"""
        sale = dict(
            item_name='sugar',
            unit_price=1000,
            quantity=10,
            total=10000
        )

        response = self.tester.post(
            '/api/v1/sales',
            content_type='application/json',
            data=json.dumps(sale)
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'Sold!')
        self.assertEqual(response.status_code, 201)

    def test_add_answer_with_missing_fields(self):
        """Test that a user cannot make a sale with missing fields"""
        sale = dict(
            item_name='',
            unit_price=1000,
            quantity=10
        )

        response = self.tester.post(
            '/api/v1/sales',
            content_type='application/json',
            data=json.dumps(sale)
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'],
                         'One of the required fields is empty!')
        self.assertEqual(response.status_code, 400)

    def test_user_cannot_add_sale_with_non_digits(self):
        """Test that a user cannot add a sale with non digits"""
        sale = dict(
            item_name='sugar',
            unit_price='one thousand',
            quantity='ten'
        )

        response = self.tester.post(
            '/api/v1/sales',
            content_type='application/json',
            data=json.dumps(sale)
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'],
                         'Quantity and unit price should be numbers!')
        self.assertEqual(response.status_code, 400)
