from sqlite3 import Error
from sqlite3 import Connection as Conn
import sqlite3
import os

class DataBase():
    def __init__(self):
        self.name = 'Scoreboard'
        self.path = "{0}\{1}\{2}.db".format(os.getcwd(), 'Data', self.name)
        self.conn : Conn = self.createConnection(self.path)

    def createConnection(self, db_file):
        """ create a database connection to a SQLite database """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            #print("SQLite: ", sqlite3.version)
            return conn
        except Error as e:
            print(e)
                
    def closeConn(self):
        if self.conn:
            self.conn.close()

    def createTable(self, sqlStatement: str):
        """ create a table from the create_table_sql statement  """
        try:
            cur = self.conn.cursor()
            cur.execute(sqlStatement)
        except Error as e:
            print(e)

    def queryData(self, sqlStatement: str) -> list:
        """ Query all rows in a table """
        try:
            cur = self.conn.cursor()
            cur.execute(sqlStatement)
            rows = cur.fetchall()
            return rows
        except Error as e:
            print(e)

    def queryDataParams(self, sqlStatement: str, *values) -> list:
        """ Query all rows in a table """
        try:
            cur = self.conn.cursor()
            cur.execute(sqlStatement, values)
            rows = cur.fetchall()
            return rows
        except Error as e:
            print(e)
        finally:
            self.closeConn()

    def queryOne(self, sqlStatement: str):
        """ Query all rows in a table """
        try:
            cur = self.conn.cursor()
            cur.execute(sqlStatement)
            return cur.fetchone()[0]
        except Error as e:
            print(e)

    def insert(self, sqlStatement: str, *values):
        """ create a table from the create_table_sql statement  """
        try:
            cur = self.conn.cursor()
            param = tuple(values)
            cur.execute(sqlStatement, param)
            return cur.lastrowid
        except Error as e:
            print(e)

    def insertMany(self, sqlStatement: str, parameters):
        """ create a table from the create_table_sql statement  """
        try:
            cur = self.conn.cursor()
            cur.executemany(sqlStatement, parameters)
            self.conn.commit()
            print("Inserted values successfully")
        except Error as e:
            print(e)

    def updateData(self, sqlStatement: str, *values):
        """ create a table from the create_table_sql statement  """
        try:
            cur = self.conn.cursor()
            cur.execute(sqlStatement, values)
            self.conn.commit()
        except Error as e:
            print(e)
