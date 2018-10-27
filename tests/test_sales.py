import unittest
from api import app
from flask import json
from api.models import Sale


class TestSale(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client(self)

    def test_add_sale(self):
        """Test that a sales can be added"""
        sale = dict(
            name='sugar',
            unit_price=1000,
            quantity=10
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
            name='',
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
            name='sugar',
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

    def test_view_sales(self):
        """Test that a user can view all sales records"""
        sale = dict(
            name='sugar',
            unit_price=1000,
            quantity=10
        )

        response = self.tester.post(
            '/api/v1/sales',
            content_type='application/json',
            data=json.dumps(sale)
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'Sold!')
        self.assertEqual(response.status_code, 201)

        response = self.tester.get(
            '/api/v1/sales'
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'Sales fetched successfully!')
        self.assertEqual(response.status_code, 200)

    def test_view_sales_from_empty_list(self):
        """Test that a user cannot view sales if there are not any"""
        response = self.tester.get(
            '/api/v1/sales'
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'No sales yet!')
        self.assertEqual(response.status_code, 400)

    def test_view_individual_sale(self):
        """Test that user can view individual sale record"""
        sale = dict(
            name='sugar',
            unit_price=1000,
            quantity=10
        )

        response = self.tester.post(
            '/api/v1/sales',
            content_type='application/json',
            data=json.dumps(sale)
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'Sold!')
        self.assertEqual(response.status_code, 201)

        response = self.tester.get(
            '/api/v1/sales/1'
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'Sale fetched!')
        self.assertEqual(response.status_code, 200)

    def test_view_single_sale_without_sales(self):
        """Test that a user cannot view a single sale without any sales"""
        response = self.tester.get(
            '/api/v1/sales/1'
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'No sales yet!')
        self.assertEqual(response.status_code, 404)

    def test_view_single_sale_which_does_not_exist(self):
        """Test that user cannot sale which does not exist"""
        sale = dict(
            name='sugar',
            unit_price=1000,
            quantity=10
        )

        response = self.tester.post(
            '/api/v1/sales',
            content_type='application/json',
            data=json.dumps(sale)
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'Sold!')
        self.assertEqual(response.status_code, 201)

        response = self.tester.get(
            '/api/v1/sales/2'
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'This sale does not exist!')
        self.assertEqual(response.status_code, 404)

    def tearDown(self):
        Sale.sales.clear()
