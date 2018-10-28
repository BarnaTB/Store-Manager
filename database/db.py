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
                    name TEXT NOT NULL PRIMARY KEY,
                    quantity INTEGER NOT NULL,
                    unit_price INTEGER NOT NULL
                    );
                """
            )

            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS sales (
                    sales_id SERIAL PRIMARY KEY,
                    sale_author TEXT NOT NULL,
                    name TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    unit_price INTEGER NOT NULL,
                    total_price INTEGER NOT NULL,
                    purchase_date TEXT NOT NULL
                    );
                """
            )

            print('Connected to {}!'.format(self.db))
        except Exception as e:
            print(e)
            print('Failed to connect to database!')

    def insert_product(self, name, quantity, unit_price):
        """SQL query to add a product to the database"""

        insert_product_command = """
        INSERT INTO products(name, quantity, unit_price)\
        VALUES('{}', '{}', '{}');
        """.format(name, quantity, unit_price)
        self.cursor.execute(insert_product_command)

    def insert_user(self, username, email, password, admin):
        """Method to insert a new user to the database"""

        insert_user_command = """
        INSERT INTO users(username, email, password, admin)\
        VALUES ('{}', '{}', '{}', '{}');
        """.format(username, email, password, admin)
        self.cursor.execute(insert_user_command)

    def insert_sale(self, *args):
        """Method to insert a sales record to the database"""

        author = args[0]
        name = args[1]
        quantity = args[2]
        unit_price = args[3]
        total = args[4]
        date = args[5]

        insert_sale_command = """
        INSERT INTO sales(sale_author, name, quantity, unit_price,\
        total_price, purchase_date) VALUES (\
        '{}', '{}', '{}', '{}', '{}', '{}');
        """.format(author, name, quantity, unit_price, total, date)
        self.cursor.execute(insert_sale_command)

    def query(self, table, column, value):
        """Method to query user by their username"""

        query_user_command = """
        SELECT * FROM {} WHERE {}='{}';
        """.format(table, column, value)
        self.cursor.execute(query_user_command)
        row = self.cursor.fetchone()

        return row

    def query_all(self, table):
        """Method enables user to retrieve all rows in a table"""

        query_command = """
        SELECT * FROM {};
        """.format(table)
        self.cursor.execute(query_command)
        rows = self.cursor.fetchall()

        return rows

    def update(self, *args):
        """Method to make a normal user an admin"""
        table = args[0]
        column = args[1]
        new_status = args[2]
        cell = args[3]
        value = args[4]

        update_command = """
        UPDATE {} SET {}='{}' WHERE {}='{}';
        """.format(table, column, new_status, cell, value)
        self.cursor.execute(update_command)

    def update_many(self, name, quantity, unit_price, product_id):
        """Method to make update multiple columns"""

        update_many_command = """
        UPDATE products SET name='{}', quantity='{}', unit_price='{}'\
        WHERE product_id='{}';
        """.format(name, quantity, unit_price, product_id)
        self.cursor.execute(update_many_command)

    def drop_table(self, table_name):
        """Method to drop tables"""
        drop_table_command = """
        DROP TABLE {};
        """.format(table_name)
        self.cursor.execute(drop_table_command)
