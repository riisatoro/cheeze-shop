import sqlite3
import uuid

from database.models import UserFromDB, RegistrationUser, UserToDB
from schemas import Product, Order


class DBConnection:
    def __init__(self, db_name: str = "./database/database.sqlite"):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        return self.conn.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()


class DBManager:
    @staticmethod
    def create_database(cursor: sqlite3.Cursor):
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL,
                folder_hash TEXT NOT NULL,
                is_admin BOOLEAN DEFAULT FALSE,
                CONSTRAINT unique_email UNIQUE(email),
                CONSTRAINT unique_username UNIQUE(username)
            );
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                price REAL NOT NULL,
                image TEXT NULL,
                stock REAL NULL
            );
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                request_id INTEGER NOT NULL
            );
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders (id),
                FOREIGN KEY (product_id) REFERENCES products (id)
            );
            """
        )

    @staticmethod
    def create_user(cursor: sqlite3.Cursor, user: RegistrationUser):
        user = UserToDB(**user.model_dump(), folder_hash=uuid.uuid4().hex)
        cursor.execute(
            """
            INSERT INTO users (username, email, password, folder_hash, is_admin) VALUES (?, ?, ?, ?, ?);
            """,
            (user.username, user.email, user.password, user.folder_hash, user.is_admin)
        )

    @staticmethod
    def get_user_by_email(cursor: sqlite3.Cursor, email: str) -> UserFromDB:
        cursor.execute(
            """
            SELECT * FROM users WHERE email = ?;
            """,
            (email,)
        )
        user_tuple = cursor.fetchone()
        fields = list(UserFromDB.__fields__.keys())
        return UserFromDB(**{fields[index]: value for index, value in enumerate(user_tuple) })


    @staticmethod
    def get_product_list(cursor: sqlite3.Cursor) -> list[Product]:
        cursor.execute(
            """
            SELECT * FROM products;
            """
        )
        products_tuple = cursor.fetchall()
        fields = list(Product.__fields__.keys())
        return [
            Product(
                **{fields[index]: value for index, value in enumerate(product_tuple)}
            )
            for product_tuple in products_tuple
        ]


    @staticmethod
    def get_product_by_id(cursor: sqlite3.Cursor, product_id: int):
        cursor.execute(
            """
            SELECT * FROM products WHERE id = ?;
            """,
            (product_id,)
        )
        product_tuple = cursor.fetchone()
        fields = list(Product.__fields__.keys())
        return Product(**{fields[index]: value for index, value in enumerate(product_tuple) })

    @staticmethod
    def create_product(cursor: sqlite3.Cursor, product):
        cursor.execute(
            """
            INSERT INTO products (name, description, price, stock) VALUES (?, ?, ?, ?);
            """,
            (product.name, product.description, product.price, product.stock)
        )

    @staticmethod
    def patch_product(cursor: sqlite3.Cursor, product_id, patch_fields):
        product = DBManager.get_product_by_id(cursor, product_id)
        product = product.model_copy(update=patch_fields)
        cursor.execute(
            """
            UPDATE products SET name = ?, description = ?, price = ?, image = ?, stock = ? WHERE id = ?;
            """,
            (product.name, product.description, product.price, product.image, product.stock, product.id)
        )

    @staticmethod
    def get_order(cursor: sqlite3.Cursor, request_id: int):
        cursor.execute(
            """
            SELECT * FROM orders WHERE request_id = ?;
            """,
            (request_id,)
        )
        order_tuple = cursor.fetchone()
        if not order_tuple:
            return None

        fields = list(Order.__fields__.keys())
        return Order(**{fields[index]: value for index, value in enumerate(order_tuple) })

    @staticmethod
    def create_order(cursor: sqlite3.Cursor, request_id: int):
        cursor.execute(
            """
            INSERT INTO orders (request_id) VALUES (?);
            """,
            (request_id,)
        )
        return DBManager.get_order(cursor, request_id)

    @staticmethod
    def create_order_item(cursor: sqlite3.Cursor, order_id: int, order_details):
        cursor.execute(
            """
            INSERT INTO order_items (order_id, product_id, quantity) VALUES (?, ?, ?);
            """,
            (order_id, order_details.product_id, order_details.quantity)
        )

    @staticmethod
    def get_order_items(cursor: sqlite3.Cursor, order_id: int):
        cursor.execute(
            """
            SELECT * FROM order_items WHERE order_id = ?;
            """,
            (order_id,)
        )
        order_items_tuple = cursor.fetchall()

        items = []
        for item in order_items_tuple:
            product = DBManager.get_product_by_id(cursor, item[2])
            items.append((item[0], product, item[3], item[3] * product.price))

        return items
