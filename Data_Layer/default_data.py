import os, sys

FULL_PATH = os.getcwd()
sys.path.append(FULL_PATH)

from Data_Layer.data_base import DataBase
from sqlite3 import Error

class DefaultData():
  def __init__(self):
    self.db = DataBase()
    self.conn = self.db.conn
    self._tablePlayer = '''
                    CREATE TABLE IF NOT EXISTS Player (
                      id_player INTEGER PRIMARY KEY,
                      name VARCHAR(6) NOT NULL,
                      CHECK (LENGTH(name) >= 3 AND LENGTH(name) <= 8)
                    );
                  '''
    self._tableGame = '''
                    CREATE TABLE IF NOT EXISTS Game (
                      id_game INTEGER PRIMARY KEY,
                      start_date DATETIME NOT NULL,
                      end_date DATETIME NOT NULL,
                      difficulty INTEGER NOT NULL
                    );
                '''
    self._tableScore = '''
                    CREATE TABLE IF NOT EXISTS Score (
                      id_score INTEGER PRIMARY KEY,
                      score INTEGER NOT NULL,
                      id_game INTEGER NOT NULL,
                      FOREIGN KEY (id_game) REFERENCES Game(Id_game)
                    );
                  '''
    self._tablePlayerScore = '''
                    CREATE TABLE IF NOT EXISTS Player_Score (
                      player_score_id INTEGER PRIMARY KEY,
                      player_id INTEGER NOT NULL,
                      score_id INTEGER NOT NULL,
                      FOREIGN KEY (player_id) REFERENCES Player(id_player),
                      FOREIGN KEY (score_id) REFERENCES Score(id_score)
                    );
                    '''
    self._playerQuery = 'INSERT INTO Player (name) VALUES (?), (?), (?), (?)'
    self._countRows = 'SELECT COUNT(*) FROM Player'

  def createTables(self):
    try:
        # Begin a transaction
        self.conn.execute('BEGIN')

        # Perform SQL operations
        # Create tables
        self.db.createTable(self._tablePlayer)
        self.db.createTable(self._tableGame)
        self.db.createTable(self._tableScore)
        self.db.createTable(self._tablePlayerScore)

        # Insert default values if the Player table is empty
        rowCount = self.db.queryOne(self._countRows)
        if rowCount == 0:
          self.db.insert(self._playerQuery, 'Player-1', 'Player-2', 'AI-A3C', 'AI-DQN')
          print('Tables created successfully')

        # Commit the transaction
        self.conn.execute('COMMIT')

    except Error as e:
        # Rollback the transaction if an error occurred
        print('Tables cannot be created')
        print("SQLite error:", e)
        self.conn.execute('ROLLBACK')

    finally:
        # Close the database connection
        self.db.closeConn()

if __name__ == '__main__':
    db = DefaultData()
    db.createTables()

