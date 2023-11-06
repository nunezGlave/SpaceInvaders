import os, sys

FULL_PATH = os.getcwd()
sys.path.append(FULL_PATH)

from Data_Layer.data_base import DataBase

# Create database instance
bd = DataBase('Scoreboard')

# Tables's SQL statements
tableGame = '''
                CREATE TABLE IF NOT EXISTS Game (
                  id_game INTEGER PRIMARY KEY,
                  start_date DATETIME NOT NULL,
                  end_date DATETIME NOT NULL
                );
            '''

tablePlayer = '''
                CREATE TABLE IF NOT EXISTS Player (
                  id_player INTEGER PRIMARY KEY,
                  name VARCHAR(6) NOT NULL,
                  CHECK (LENGTH(name) >= 3 AND LENGTH(name) <= 6)
                );
              '''

tableScore = '''
                CREATE TABLE IF NOT EXISTS Score (
                  id_score INTEGER PRIMARY KEY,
                  score INTEGER NOT NULL,
                  id_game INTEGER NOT NULL,
                  FOREIGN KEY (id_game) REFERENCES Game(Id_game)
                );
              '''

tablePlayerScore = '''
                CREATE TABLE IF NOT EXISTS Player_Score (
                  player_score_id INTEGER PRIMARY KEY,
                  player_id INTEGER NOT NULL,
                  score_id INTEGER NOT NULL,
                  FOREIGN KEY (player_id) REFERENCES Player(id_player),
                  FOREIGN KEY (score_id) REFERENCES Score(id_score)
                );
                '''

# Create tables
bd.createTable(tableGame)
bd.createTable(tablePlayer)
bd.createTable(tableScore)
bd.createTable(tablePlayerScore)

# Insert default values into tables
sqlPlayers = 'INSERT INTO Player (name) VALUES (?), (?), (?), (?), (?)'
bd.insertOne(sqlPlayers, ('ZQWRT'), ('KPMNJ'), ('LVYXZ'), ('HRGTP'), ('BDJQW'))


sqlGame = 'INSERT INTO Game (start_date, end_date) VALUES (?, ?)'
gameParameters = [('2023-11-01 10:00:00 AM', '2023-11-01 10:02:00 AM'),
                  ('2023-11-02 03:15:00 PM', '2023-11-02 03:18:00 PM'),
                  ('2023-11-03 07:30:00 PM', '2023-11-03 07:35:00 PM'),
                  ('2023-11-04 08:10:00 AM', '2023-11-04 08:17:00 AM')]
bd.insertMany(sqlGame, gameParameters)


sqlScore = 'INSERT INTO Score (score, id_game) VALUES (?, ?)'
scoreParameters = [(250, 1),
                    (800, 2),
                    (1500, 3),
                    (3100, 4)]
bd.insertMany(sqlScore, scoreParameters)


sqlPlayerScore= 'INSERT INTO Player_Score (player_id, score_id) VALUES (?, ?)'
PlayerScoreParameters = [(1, 1),
                          (2, 2),
                          (3, 3),
                          (4, 4)]
bd.insertMany(sqlPlayerScore, PlayerScoreParameters)

# Close database's connection
bd.closeConnection()





