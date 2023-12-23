from Data_Layer.data_base import DataBase
from sqlite3 import Error

class GameData():
    def __init__(self):
        self.db = DataBase()
        self.conn = self.db.conn
        self._gameQuery = 'INSERT INTO Game (start_date, end_date, difficulty) VALUES (?, ?, ?)'
        self._scoreQuery = 'INSERT INTO Score (score, id_game) VALUES (?, ?)'
        self._playerScoreQuery = 'INSERT INTO Player_Score (player_id, score_id) VALUES (?, ?)'
        self._bestScoreQuery1 = '''
                            SELECT G.id_game AS gameID, PL.name AS player, S.score, PLS.score_id, difficulty
                            FROM Player AS PL
                            JOIN Player_Score AS PLS ON PL.id_player = PLS.player_id
                            JOIN Score AS S ON PLS.score_id = S.id_score
                            JOIN Game AS G ON S.id_game = G.id_game
                            JOIN (
                                SELECT score_id
                                FROM Player_Score
                                GROUP BY score_id
                                HAVING COUNT(*) = 1
                            ) AS subquery ON PLS.score_id = subquery.score_id
                            WHERE PL.id_player = ? and difficulty = ?
                            ORDER BY S.score DESC
                            Limit 1
                            '''
        self._bestScoreQuery2 = '''
                        SELECT 
                        G.id_game AS gameID, PL.name AS player, S.score, PLS.score_id, difficulty
                        FROM Player AS PL
                        JOIN Player_Score AS PLS ON PL.id_player = PLS.player_id
                        JOIN Score AS S ON PLS.score_id = S.id_score
                        JOIN Game AS G ON S.id_game = G.id_game
                        WHERE PL.id_player IN (?, ?)
                        AND EXISTS (
                            SELECT 1
                            FROM Player_Score AS PS
                            WHERE PS.score_id = PLS.score_id
                            AND PS.player_id IN (?, ?)
                            GROUP BY PS.score_id
                            HAVING COUNT(DISTINCT PS.player_id) = 2
                        )
                        AND difficulty = ?
                        ORDER BY S.score DESC
                        Limit 1
                        '''

    def saveGame(self, startTime: str, endTime: str, difficulty: bool, score: int, players: list):
        try:
            # Begin a transaction
            self.conn.execute('BEGIN')

            # Perform SQL operations
            gameId = self.db.insert(self._gameQuery, startTime, endTime, difficulty)
            scoreId = self.db.insert(self._scoreQuery, score, gameId)
            for player in players:
                self.db.insert(self._playerScoreQuery, player.id, scoreId)

            # Commit the transaction
            self.conn.execute('COMMIT')
            print('Game saved successfully')

        except Error as e:
            # Rollback the transaction if an error occurred
            print('The game cannot be saved')
            print("SQLite error:", e)
            self.conn.execute('ROLLBACK')

        finally:
            # Close the database connection
            self.db.closeConn()

    def scoreSinglePlayer(self, idPlayer: int, difficulty: bool):
        result = self.db.queryDataParams(self._bestScoreQuery1, idPlayer, difficulty)
        return result

    def scoreMultiPlayer(self, idPlayer1: int, idPlayer2: int, difficulty: bool):
        result = self.db.queryDataParams(self._bestScoreQuery2, idPlayer1, idPlayer2, idPlayer1, idPlayer2, difficulty)
        return result