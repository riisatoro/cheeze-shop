import sqlite3


class DBConnection:
    def __init__(self, db_name: str = "./database/database.sqlite"):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        return self.conn.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
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
                folder_hash TEXT NOT NULL
            );
            """
        )
