import sqlite3

class Database:
    def __init__(self, db_file):
        self.db_file = db_file

    def _connect(self):
        conn = sqlite3.connect(self.db_file)
        return conn

    def create_table(self):
        with self._connect() as conn:
            cursor = conn.cursor()
            query = '''CREATE TABLE IF NOT EXISTS users ( "id"	INTEGER NOT NULL, "name"	TEXT NOT NULL, 
            "email"	TEXT NOT NULL, "number"	INTEGER NOT NULL, "admin"	INTEGER NOT NULL );'''
            cursor.execute(query)
            conn.commit()

    def add_user(self, id, username, email, number):
        with self._connect() as conn:
            cursor = conn.cursor()
            query = 'INSERT INTO users (id, name, email, number, admin) VALUES (?, ?, ?, ?, ?);'
            cursor.execute(query, (id, username, email, number, 0))
            conn.commit()

    def get_users(self):
        with self._connect() as conn:
            cursor = conn.cursor()
            query = 'SELECT * FROM users;'
            cursor.execute(query)
            return cursor.fetchall()

    def close(self):
        pass  # Закрывать ничего не нужно, так как каждое подключение открывается и закрывается отдельно