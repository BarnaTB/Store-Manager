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
                dbname=self.db,
                user='postgres',
                password='##password',
                host='localhost'
            )

            self.cursor = self.connection.cursor()
            self.connection.autocommit = True

            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS user (
                    user_id SERIAL PRIMARY KEY,
                    username TEXT NOT NULL,
                    email TEXT NOT NULL,
                    password TEXT NOT NULL,
                    admin BOOL DEFAULT
                    )
                """
            )

            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS product (
                    product_id SERIAL PRIMARY KEY,
                    product_name TEXT NOT NULL,
                    quantity TEXT NOT NULL,
                    unit_price TEXT NOT NULL
                    )
                """
            )

            print('Connected to {}!'.format(self.db))
        except psycopg2.Error as e:
            print(e)
            print('Failed to connect to database!')
