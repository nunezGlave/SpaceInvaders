from sqlite3 import Error
from sqlite3 import Connection as Conn
import sqlite3
import os

class DataBase():
    def __init__(self, dbName: str):
        self.path = "{0}\{1}\{2}.db".format(os.getcwd(), 'Data_Base', dbName)
        self.conn : Conn = self.createConnection(self.path)

    def createConnection(self, db_file):
        """ create a database connection to a SQLite database """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            print("SQLite: ", sqlite3.version)
            return conn
        except Error as e:
            print(e)
                
    def closeConnection(self):
        if self.conn:
            self.conn.close()

    def createTable(self, sqlStatement: str):
        """ create a table from the create_table_sql statement  """
        try:
            cur = self.conn.cursor()
            cur.execute(sqlStatement)
            self.conn.commit()
            print('Table created successfully')
        except Error as e:
            print(e)

    def queryData(self, sqlStatement: str):
        """ Query all rows in a table """
        try:
            cur = self.conn.cursor()
            cur.execute(sqlStatement)
            rows = cur.fetchall()
            return rows
        except Error as e:
            print(e)

    def insertOne(self, sqlStatement: str, *values):
        """ create a table from the create_table_sql statement  """
        try:
            cur = self.conn.cursor()
            cur.execute(sqlStatement, values)
            self.conn.commit()
            print("Inserted values successfully")
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
