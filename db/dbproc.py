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
            query = '''CREATE TABLE IF NOT EXISTS "values" ( "id" INTEGER NOT NULL, "weight"	INTEGER NOT NULL,
	        "city"	TEXT NOT NULL, "product" TEXT NOT NULL)'''
            cursor.execute(query)
            query = '''CREATE TABLE IF NOT EXISTS "walls" ("id"	INTEGER NOT NULL, "luggageStorage"	INTEGER NOT NULL, "auxiliaryRoom"	INTEGER,
	        "isolation"	INTEGER, "engineRoom"	INTEGER, "official"	INTEGER)'''
            cursor.execute(query)
            conn.commit()

    def add_user(self, id, username, email, number):
        with self._connect() as conn:
            cursor = conn.cursor()
            query = '''SELECT 1 FROM users WHERE id = ? '''
            data = (id,)
            result = cursor.fetchone()
            if result:
                query = 'INSERT INTO users (id, name, email, number, admin) VALUES (?, ?, ?, ?, ?);'
                cursor.execute(query, (id, username, email, number, 0))
                conn.commit()
                return True
            else:
                return False

    def get_users(self):
        with self._connect() as conn:
            cursor = conn.cursor()
            query = 'SELECT * FROM users;'
            cursor.execute(query)
            return cursor.fetchall()

    def add_values(self, id, weight, city, product):
        with self._connect() as conn:
            cursor = conn.cursor()
            query = 'INSERT INTO "values" (id, city, weight, product) VALUES (?, ?, ?, ?);'
            cursor.execute(query, (id, city, weight , product))
            conn.commit()

    def get_values(self):
        with self._connect() as conn:
            cursor = conn.cursor()
            query = f'SELECT * FROM "values" WHERE id = {773794732};'
            cursor.execute(query)
            return cursor.fetchall()

    def close(self):
        pass