''' Created by Alexander '''

import os, sys

# Add the project root directory to sys.path
FULL_PATH = os.getcwd()
sys.path.append(FULL_PATH)

# Import libraries
from pygame import *
from Logical_Layer.Viewport.screen_surface import Screen
from Logical_Layer.Util.text import Text
from Logical_Layer.Util.color import Color
from Logical_Layer.Util.align import Align
from Data_Layer.data_base import DataBase

def should_exit(evt):
    return evt.type == QUIT or (evt.type == KEYUP and evt.key == K_ESCAPE)

if __name__ == '__main__':
    # Variables to control the game
    gameControl = True
    listColor = Color()

    # Start the video game
    init()
    clock = time.Clock()
    display.set_caption('Space Invaders')

    # Set main screen dimensions
    window = display.set_mode((display.Info().current_w , display.Info().current_h))
    screen = Screen(window)
    screen.surface.fill(listColor.WHITE)
     
    # Font letter
    FONT_PATH = FULL_PATH + '/Assets/Fonts/'
    FONT = FONT_PATH + 'space_invaders.ttf'

    # Create Text variables
    title = Text('SCOREBOARD', FONT, 40, listColor.BLUE, screen.widthP(50), screen.heightP(20), Align.CENTER)      
    header = Text('Player {0} Score'.format(" " * 42),FONT, 35, listColor.BLACK, screen.widthP(50), title.textHeight + 25, Align.CENTER)
    
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
    numSpaces = 55
    for index, result in enumerate(results):
        format = "{0}{1}{2}".format(result[0], " " * numSpaces, result[1])
        row = Text(format, FONT, 30, listColor.BLUE, screen.widthP(50), header.textHeight + 10 + (index * 70), Align.CENTER)
        listScores.append(row)

    # Render games 
    while gameControl:
        # Draw texts
        title.draw(window)
        header.draw(window)
        for score in listScores:
            score.draw(window)

        # Update content
        display.update()

        for e in event.get():
            if should_exit(e):
                sys.exit()

        clock.tick(60)

