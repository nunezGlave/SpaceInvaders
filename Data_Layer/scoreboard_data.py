from Data_Layer.data_base import DataBase

class ScoreData():
    def __init__(self):
        self.db = DataBase()
        self.conn = self.db.conn
        self._singleplayerQuery = '''
                SELECT ROW_NUMBER() OVER (ORDER BY S.score DESC) as 'game', name as player, S.score as score
                FROM Player as PL
                JOIN Player_Score as PLS ON PL.id_player = PLS.player_id
                JOIN Score as S ON PLS.score_id = S.id_score
                JOIN Game as G ON S.id_game = G.id_game
				JOIN (
					SELECT score_id
					FROM Player_Score
					GROUP BY score_id
					HAVING COUNT(*) = 1
				) AS subquery ON PLS.score_id = subquery.score_id
				WHERE difficulty = ?
				ORDER BY S.score DESC
                LIMIT 5;
            '''
        self._multiplayerQuery = '''
                SELECT ROW_NUMBER() OVER (ORDER BY S.score DESC) as 'game', 
                       PL1.name || '  &  ' || PL2.name as players, S.score AS score
                FROM Player_Score AS PLS1
                JOIN Player AS PL1 ON PLS1.player_id = PL1.id_player
                JOIN Score AS S ON PLS1.score_id = S.id_score
                JOIN Game AS G ON S.id_game = G.id_game
                JOIN Player_Score AS PLS2 ON G.id_game = PLS2.score_id AND PLS1.player_id < PLS2.player_id
                JOIN Player AS PL2 ON PLS2.player_id = PL2.id_player
                JOIN (
                    SELECT score_id
                    FROM Player_Score
                    GROUP BY score_id
                    HAVING COUNT(*) = 2
                ) AS subquery ON PLS1.score_id = subquery.score_id
                WHERE G.difficulty = ?
                ORDER BY S.score DESC
                LIMIT 5;
            '''

    def singlePlayer(self, difficulty: bool):
        results = self.db.queryDataParams(self._singleplayerQuery, difficulty)
        return results
    
    def multiPlayer(self, difficulty: bool):
        results = self.db.queryDataParams(self._multiplayerQuery, difficulty)
        return results