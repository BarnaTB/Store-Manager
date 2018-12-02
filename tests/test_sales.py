import unittest
from api import app
from flask import json
from api.models import Sale
from database.db import DatabaseConnection
from base_test import BaseTest


class TestSale(BaseTest):
    def setUp(self):
        self.tester = app.test_client(self)
        self.db = DatabaseConnection()

    def test_attendant_add_sale(self):
        """Test that a sales record can be added by attendant"""
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
            category='groceries',
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

        self.assertEqual(reply['message'], 'Product added successfully!')
        self.assertEqual(response.status_code, 201)

        reply = self.login_user()
        token = reply['token']

        user = dict(
            username='barna',
            email='barna@store.com',
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

        token = reply['token']

        sale = dict(
            name='sugar',
            quantity=10
        )

        response = self.tester.post(
            '/api/v1/sales',
            content_type='application/json',
            data=json.dumps(sale),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'Sold!')
        self.assertEqual(response.status_code, 201)

    def test_add_sale_with_missing_fields(self):
        """Test that a user cannot make a sale with missing fields"""
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
            category='groceries',
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

        self.assertEqual(reply['message'], 'Product added successfully!')
        self.assertEqual(response.status_code, 201)

        reply = self.login_user()
        token = reply['token']

        user = dict(
            username='barna',
            email='barna@store.com',
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

        token = reply['token']

        sale = dict(
            name='',
            quantity=10
        )

        response = self.tester.post(
            '/api/v1/sales',
            content_type='application/json',
            data=json.dumps(sale),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'],
                         'One of the required fields is empty!')
        self.assertEqual(response.status_code, 400)

    def test_user_cannot_add_sale_with_non_digits(self):
        """Test that a user cannot add a sale with non digits"""
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
            category='groceries',
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

        self.assertEqual(reply['message'], 'Product added successfully!')
        self.assertEqual(response.status_code, 201)

        reply = self.login_user()
        token = reply['token']

        user = dict(
            username='barna',
            email='barna@store.com',
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

        token = reply['token']

        sale = dict(
            name='sugar',
            quantity='ten'
        )

        response = self.tester.post(
            '/api/v1/sales',
            content_type='application/json',
            data=json.dumps(sale),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'Quantity should be a number!')
        self.assertEqual(response.status_code, 400)

    def test_sell_a_product_which_does_not_exist(self):
        """Test that attendant cannot sell non-existent product"""
        reply = self.login_user()
        token = reply['token']

        user = dict(
            username='barna',
            email='barna@store.com',
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

        token = reply['token']

        sale = dict(
            name='sugar',
            quantity=10
        )

        response = self.tester.post(
            '/api/v1/sales',
            content_type='application/json',
            data=json.dumps(sale),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'This product does not exist!')
        self.assertEqual(response.status_code, 400)

    def test_attendant_cannot_sell_out_of_stock_product(self):
        """Test that a user cannot sell a product which is out of stock"""
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
            category='groceries',
            name='sugar',
            unit_price=1000,
            quantity=10
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

        reply = self.login_user()
        token = reply['token']

        user = dict(
            username='barna',
            email='barna@store.com',
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

        token = reply['token']

        sale = dict(
            name='sugar',
            quantity=10
        )

        response = self.tester.post(
            '/api/v1/sales',
            content_type='application/json',
            data=json.dumps(sale),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'Sold!')
        self.assertEqual(response.status_code, 201)

        sale = dict(
            name='sugar',
            quantity=10
        )

        response = self.tester.post(
            '/api/v1/sales',
            content_type='application/json',
            data=json.dumps(sale),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'Product is out of stock!')
        self.assertEqual(response.status_code, 400)

    def test_attendant_cannot_sell_more_than_stock(self):
        """Test that attendant cannot sell more than the stock"""
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
            category='groceries',
            name='sugar',
            unit_price=1000,
            quantity=10
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

        reply = self.login_user()
        token = reply['token']

        user = dict(
            username='barna',
            email='barna@store.com',
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

        token = reply['token']

        sale = dict(
            name='sugar',
            quantity=20
        )

        response = self.tester.post(
            '/api/v1/sales',
            content_type='application/json',
            data=json.dumps(sale),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'],
                         'Unfortunately we have less than you require!')
        self.assertEqual(response.status_code, 400)

    def test_view_sales(self):
        """Test that a user can view all sales records"""
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
            category='groceries',
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

        self.assertEqual(reply['message'], 'Product added successfully!')
        self.assertEqual(response.status_code, 201)

        reply = self.login_user()
        token = reply['token']

        user = dict(
            username='barna',
            email='barna@store.com',
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
            username='admin',
            password='Pass1234'
        )

        response = self.tester.post(
            '/api/v1/login',
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())

        token = reply['token']

        sale = dict(
            name='sugar',
            quantity=10
        )

        response = self.tester.post(
            '/api/v1/sales',
            content_type='application/json',
            data=json.dumps(sale),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'Sold!')
        self.assertEqual(response.status_code, 201)

        response = self.tester.get(
            '/api/v1/sales',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'Sales fetched successfully!')
        self.assertEqual(response.status_code, 200)

    def test_attendant_view_sales(self):
        """Test that attendant cannot view all sales records"""
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
            category='groceries',
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

        self.assertEqual(reply['message'], 'Product added successfully!')
        self.assertEqual(response.status_code, 201)

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

        token = reply['token']

        sale = dict(
            name='sugar',
            quantity=10
        )

        response = self.tester.post(
            '/api/v1/sales',
            content_type='application/json',
            data=json.dumps(sale),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'Sold!')
        self.assertEqual(response.status_code, 201)

        reply = self.login_user()
        token = reply['token']

        reply = self.login_user()
        token = reply['token']

        user = dict(
            username='barna',
            email='barna@store.com',
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
        token = reply['token']

        response = self.tester.get(
            '/api/v1/sales',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'],
                         'You are not authorized to access this!')
        self.assertEqual(response.status_code, 503)

    def test_view_sales_from_empty_table(self):
        """Test that a user cannot view sales if there are not any"""
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
            category='groceries',
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

        self.assertEqual(reply['message'], 'Product added successfully!')
        self.assertEqual(response.status_code, 201)

        reply = self.login_user()
        token = reply['token']

        user = dict(
            username='barna',
            email='barna@store.com',
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
            username='admin',
            password='Pass1234'
        )

        response = self.tester.post(
            '/api/v1/login',
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())

        token = reply['token']

        response = self.tester.get(
            '/api/v1/sales',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'No sales yet!')
        self.assertEqual(response.status_code, 400)

    def test_view_individual_sale(self):
        """Test that user can view individual sale record"""
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
            category='groceries',
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

        self.assertEqual(reply['message'], 'Product added successfully!')
        self.assertEqual(response.status_code, 201)

        reply = self.login_user()
        token = reply['token']

        user = dict(
            username='barna',
            email='barna@store.com',
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
            username='admin',
            password='Pass1234'
        )

        response = self.tester.post(
            '/api/v1/login',
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())

        token = reply['token']

        sale = dict(
            name='sugar',
            quantity=10
        )

        response = self.tester.post(
            '/api/v1/sales',
            content_type='application/json',
            data=json.dumps(sale),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'Sold!')
        self.assertEqual(response.status_code, 201)

        response = self.tester.get(
            '/api/v1/sales/1',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'Sale fetched!')
        self.assertEqual(response.status_code, 200)

    def test_view_single_sale_without_sales(self):
        """Test that a user cannot view a single sale without any sales"""
        reply = self.login_user()
        token = reply['token']

        user = dict(
            username='barna',
            email='barna@store.com',
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

        token = reply['token']

        response = self.tester.get(
            '/api/v1/sales/1',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'No sales yet!')
        self.assertEqual(response.status_code, 400)

    def test_view_single_sale_which_does_not_exist(self):
        """Test that user cannot sale which does not exist"""
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
            category='groceries',
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

        self.assertEqual(reply['message'], 'Product added successfully!')
        self.assertEqual(response.status_code, 201)

        reply = self.login_user()
        token = reply['token']

        user = dict(
            username='barna',
            email='barna@store.com',
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
            username='admin',
            password='Pass1234'
        )

        response = self.tester.post(
            '/api/v1/login',
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())

        token = reply['token']

        sale = dict(
            name='sugar',
            quantity=10
        )

        response = self.tester.post(
            '/api/v1/sales',
            content_type='application/json',
            data=json.dumps(sale),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'Sold!')
        self.assertEqual(response.status_code, 201)

        response = self.tester.get(
            '/api/v1/sales/2',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'This sale does not exist!')
        self.assertEqual(response.status_code, 400)

    def test_attendant_gets_sale_which_does_not_belong_to_them(self):
        """Test that an attendant cannot get another's sales record"""
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
            category='groceries',
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

        self.assertEqual(reply['message'], 'Product added successfully!')
        self.assertEqual(response.status_code, 201)

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

        token = reply['token']

        sale = dict(
            name='sugar',
            quantity=10
        )

        response = self.tester.post(
            '/api/v1/sales',
            content_type='application/json',
            data=json.dumps(sale),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'Sold!')
        self.assertEqual(response.status_code, 201)

        reply = self.login_user()
        token = reply['token']

        user = dict(
            username='barna',
            email='barna@store.com',
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

        token = reply['token']

        response = self.tester.get(
            '/api/v1/sales/1',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'],
                         'You are not authorized to access this!')
        self.assertEqual(response.status_code, 503)

    def test_view_individual_sale_with_vague_id(self):
        """Test that user can view individual sale record"""
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
            category='groceries',
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

        self.assertEqual(reply['message'], 'Product added successfully!')
        self.assertEqual(response.status_code, 201)

        reply = self.login_user()
        token = reply['token']

        user = dict(
            username='barna',
            email='barna@store.com',
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
            username='admin',
            password='Pass1234'
        )

        response = self.tester.post(
            '/api/v1/login',
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())

        token = reply['token']

        sale = dict(
            name='sugar',
            quantity=10
        )

        response = self.tester.post(
            '/api/v1/sales',
            content_type='application/json',
            data=json.dumps(sale),
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'Sold!')
        self.assertEqual(response.status_code, 201)

        response = self.tester.get(
            '/api/v1/sales/the',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'The sale id should be a number!')
        self.assertEqual(response.status_code, 400)

    def tearDown(self):
        self.db.drop_table('products')
        self.db.drop_table('users')
        self.db.drop_table('sales')
