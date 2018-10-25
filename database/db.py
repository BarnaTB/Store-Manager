import psycopg2
import os


class DatabaseConnection:
    """Class handles database queries and connection"""

    def __init__(self):
        try:
            if os.getenv('APP_SETTINGS') == 'testing':
                self.db = 'test_db'
            else:
                self.db = 'storemanager_db'
            self.connection = psycopg2.connect(
                database=self.db,
                user='postgres',
                password='##password',
                host='localhost'
            )

            self.cursor = self.connection.cursor()
            self.connection.autocommit = True

            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    user_id SERIAL PRIMARY KEY,
                    username TEXT NOT NULL,
                    email TEXT NOT NULL,
                    password TEXT NOT NULL,
                    admin BOOL DEFAULT FALSE
                    );
                """
            )

            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS products (
                    product_id SERIAL,
                    product_name TEXT NOT NULL PRIMARY KEY,
                    quantity TEXT NOT NULL,
                    unit_price TEXT NOT NULL
                    );
                """
            )

            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS sales (
                    sales_id SERIAL PRIMARY KEY,
                    sale_author TEXT NOT NULL,
                    product_name TEXT NOT NULL,
                    quantity INTEGR NOT NULL,
                    total_price INTEGER NOT NULL,
                    purchase_date TIMESTAMP
                    );
                """
            )

            print('Connected to {}!'.format(self.db))
        except Exception as e:
            print(e)
            print('Failed to connect to database!')

    def insert_product(self, product_name, quantity, unit_price):
        """SQL query to add a product to the database"""

        insert_product_command = """
        INSERT INTO products(product_name, quantity, unit_price)\
        VALUES('{}', '{}', '{}');
        """.format(product_name, quantity, unit_price)
        self.cursor.execute(insert_product_command)

    def insert_user(self, username, email, password):
        """Method to insert a new user to the database"""

        insert_user_command = """
        INSERT INTO users(username, email, password) VALUES ('{}', '{}', '{}');
        """.format(username, email, password)
        self.cursor.execute(insert_user_command)
