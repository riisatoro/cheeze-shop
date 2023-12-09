import sqlite3
import uuid

from database.models import UserFromDB, RegistrationUser, UserToDB


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
                stock INTEGER NULL
            );
            """
        )


    @staticmethod
    def create_user(cursor: sqlite3.Cursor, user: RegistrationUser):
        user = UserToDB(**user.model_dump(), folder_hash=uuid.uuid4().hex)
        cursor.execute(
            """
            INSERT INTO users (username, email, password, folder_hash) VALUES (?, ?, ?, ?);
            """,
            (user.username, user.email, user.password, user.folder_hash)
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
