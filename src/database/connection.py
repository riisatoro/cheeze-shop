import sqlite3
import uuid

from database.models import User
from security import hash_password


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
                UNIQUE(email, username)
            );
            """
        )

    @staticmethod
    def create_user(cursor: sqlite3.Cursor, user: User):
        folder_hash = uuid.uuid4().hex
        password = hash_password(user.password)
        cursor.execute(
            """
            INSERT INTO users (username, email, password, folder_hash) VALUES (?, ?, ?, ?);
            """,
            (user.username, user.email, password, folder_hash)
        )
