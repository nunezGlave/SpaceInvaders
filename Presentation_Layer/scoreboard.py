''' Created by Alexander '''
# Allow individual execution file [Remove this when finished]
import os, sys
FULL_PATH = os.getcwd()
sys.path.append(FULL_PATH)

# Import libraries
from pygame import *
from Logical_Layer.Interfaces.viewport import Viewport
from Logical_Layer.Util.state import State
from Logical_Layer.Viewport.screen_surface import Screen
from Logical_Layer.Util.text import Text
from Logical_Layer.Util.color import Color
from Logical_Layer.Util.align import Align
from Data_Layer.data_base import DataBase
import pygame as py

class Scoreboard(Viewport):
    def __init__(self, difficulty: bool):
        # Initialize super class
        super().__init__("Scoreboard Menu")

        # Get attribute
        self.difficulty = difficulty

    def handle_events(self, events) -> dict:
        for event in events:
            if event.type == KEYDOWN:
                if event.key == py.K_BACKSPACE:
                    return {'state': State.PLAYER , 'difficulty': self.difficulty}
            else:
                self.exit(event)

    def draw(self):
        #Paint background
        self.screen.fill(Color.WHITE.value)

        # Font letter
        self.font = self.getFont()

        # Create Text variables
        title = Text('SCOREBOARD', self.font, 70, Color.BLUE1 if self.difficulty else Color.RED1, self.display.widthP(50), self.display.heightP(20), Align.CENTER)      
        header = Text('Player {0} Score'.format(" " * 42), self.font, 50, Color.BLACK, self.display.widthP(46), title.textHeight + 25, Align.CENTER)
        
        # Create database connection
        bd = DataBase("Scoreboard")    
        sql = '''
                SELECT Player.name as Player, Score.score as Score, Game.start_date as "Start Date", Game.end_date as "End Date"
                FROM Player 
                INNER JOIN Player_Score ON Player.id_player = Player_Score.player_id
                INNER JOIN Score ON Player_Score.score_id = Score.id_score
                INNER JOIN Game ON Score.id_game = Game.id_game
                ORDER BY Score.score DESC
                LIMIT 10;
            '''

        # Retrieve database information
        results = bd.queryData(sql)
        listScores = []

        # Create Text variables based on database's information
        numSpaces = 48
        for index, result in enumerate(results):
            format = "{0}{1}{2}".format(result[0], " " * numSpaces, result[1])
            row = Text(format, self.font, 50, Color.BLUE1 if self.difficulty else Color.RED2, self.display.widthP(44), header.textHeight + 10 + (index * 70), Align.CENTER)
            listScores.append(row)

        # Draw texts
        title.draw(self.screen)
        header.draw(self.screen)
        for score in listScores:
            score.draw(self.screen)


# Allow individual execution file [Remove this when finished]
if __name__ == "__main__":
    diffGame = False
    game = Scoreboard(False)
    game.run()


