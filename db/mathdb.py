import sqlite3

class MathDatabase:

    def __init__(self, db_file):
        self.db_file = db_file

    def _connect(self):
        conn = sqlite3.connect(self.db_file)
        return conn

    def create_tablemath(self):
        with self._connect() as conn:
            cursor = conn.cursor()
            query = '''CREATE TABLE IF NOT EXISTS "specificEnthalpy" (
	                "product"	TEXT NOT NULL,
	                "temp-20"	INTEGER,
	                "temp-18"	INTEGER,
	                "temp-15"	INTEGER,
	                "temp-12"	INTEGER,
	                "temp-10"	INTEGER,
	                "temp-8"	INTEGER,
	                "temp-5"	INTEGER,
	                "temp-3"	INTEGER,
	                "temp-2"	INTEGER,
	                "temp-1"	INTEGER,
	                "temp0"     INTEGER,
	                "temp1"     INTEGER,
	                "temp2"     INTEGER,
	                "temp4"     INTEGER,
	                "temp8"     INTEGER,
	                "temp10"	INTEGER,
	                "temp12"	INTEGER,
	                "temp15"	INTEGER,
	                "temp20"	INTEGER,
	                "temp25"	INTEGER,
	                "temp30"	INTEGER,
	                "temp35"	INTEGER,
	                "temp40"	INTEGER);'''
            cursor.execute(query)
            query = '''CREATE TABLE IF NOT EXISTS "specificLoad" (
	                "product"       TEXT NOT NULL,
	                "storageType"	TEXT NOT NULL,
	                "load"	        INTEGER NOT NULL);'''
            cursor.execute(query)
            conn.commit()

    def close(self):
        pass