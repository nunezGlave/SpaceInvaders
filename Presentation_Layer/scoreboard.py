''' Created by Alexander '''
# Allow individual execution file [Remove this when finished]
import os, sys
FULL_PATH = os.getcwd()
sys.path.append(FULL_PATH)

# Import libraries
from pygame import *
from Logical_Layer.Interfaces.viewport import Viewport
from Logical_Layer.Util.state import State
from Logical_Layer.Util.text import Text
from Logical_Layer.Util.color import Color
from Logical_Layer.Util.align import Align
from Logical_Layer.Util.image import Image
from Logical_Layer.Util.button import Button
from Data_Layer.scoreboard_data import ScoreData
import pygame as py

class Scoreboard(Viewport):
    def __init__(self, difficulty: bool):
        # Initialize super class
        super().__init__("Scoreboard Menu")

        # Get attribute and name's images
        self.difficulty = difficulty
        singularImgs = ['background.jpg', 'board_frame', 'extra_button']
        sharedImgs = ['backspace', 'enter']

        # Load images and font
        self.uniqImages = self.loadSharedImages(sharedImgs)
        self.images = self.loadSingularImages(singularImgs, self.difficulty)
        self.images =  self.images['basic'] if self.difficulty else self.images['doom']
        self.font = self.getFont()

        # Set a background image
        self.background = transform.scale(self.images['background'], (self.display.width, self.display.height))

        # Create images
        self.frame1 = Image(self.screen, self.images['board_frame'], 700, 630)
        self.frame2 = Image(self.screen, self.images['board_frame'], 700, 630)
        self.frame2.flip(True, False)

        # Create text
        self.title = Text('SCOREBOARD', self.font, 70, Color.WHITE, self.display.widthP(50), self.display.heightP(5), Align.CENTER)      
        self.headers = ['Game', 'Player', 'Score', 'Game', 'Player', 'Score']
        self.middle = (len(self.headers) // 2) - 1

        # Create buttons
        self.btnBack = Button(self.images['extra_button'], 0.4, 'Back', self.font)

    def handle_events(self, events) -> dict:
        for event in events:
            if event.type == KEYDOWN:
                if event.key == py.K_BACKSPACE:
                    return {'state': State.PLAYER , 'difficulty': self.difficulty}
            else:
                self.exit(event)

    def draw(self):
        # Draw background and frames
        self.screen.blit(self.background, (0, 0))
        self.frame1.draw(self.display.widthP(3), self.title.heightPosY + 20)
        self.frame2.draw(self.display.widthP(52), self.title.heightPosY + 20)

        # Create text
        self.subTitle1 = Text('Single Player', self.font, 55, Color.WHITE, self.frame1.rect.x + 80, self.frame1.rect.y + 35)      
        self.subTitle2 = Text('Multiplayer', self.font, 55, Color.WHITE, self.frame2.rect.x + 330, self.frame2.rect.y + 35)      

        # Draw titles
        self.title.draw(self.screen)
        self.subTitle1.draw(self.screen)
        self.subTitle2.draw(self.screen)

        # Create list of headers
        self.listHeaders = []
        headerWidth = self.subTitle1.xPos - 10
        headerHeight = self.subTitle1.heightPosY + 45
        for index, header in enumerate(self.headers):
            # Create and add Text Object into list
            headerText = Text(header, self.font, 50, Color.BLUE3 if self.difficulty else Color.RED2, headerWidth, headerHeight)
            self.listHeaders.append(headerText)

            # Evaluate the position of each column
            headerWidth += 160 if index == self.middle else 0
            headerWidth += headerText.textWidth + 85

        # Create left and right data
        self.displayTable(headerHeight, 1, self.frame1)
        self.displayTable(headerHeight, 2, self.frame2)

        # Clear headers
        self.listHeaders.clear()

        # Draw buttons
        self.btnBack.drawIcon(self.screen, self.uniqImages['backspace'], self.display.widthP(85), self.display.heightP(92))

        # Capture button click
        # if self.btnBack.mouseClick():
        #     self.eventBackspace()

    # Display table's score
    def displayTable(self, headerHeight: int , modeGame: int, frame: Image):
        # Get scoreboard's data
        db = ScoreData()
        if modeGame == 1:
            rows = db.singlePlayer(self.difficulty)
        else:
            rows = db.multiPlayer(self.difficulty)
            
        # Evaluate if data exists
        if len(rows) != 0:
            scoreHeight = headerHeight
            for row in rows:
                column = enumerate(row)
                scoreHeight += 70
                for index, data in column:
                    # Create a score text according to the column and row
                    index = len(self.headers) // 2 + index if modeGame == 2 else index
                    scoreWidth = self.listHeaders[index].xPos + self.listHeaders[index].textWidth/2
                    data = str(data).replace("Player-1", "PL1").replace("Player-2", "PL2").replace('AI-', '') if modeGame == 2 else str(data)
                    infoScore = Text(data, self.font, 50, Color.WHITE, scoreWidth, scoreHeight, Align.CENTER)
                   
                    # Draw header and score text
                    self.listHeaders[index].draw(self.screen)
                    infoScore.draw(self.screen)
        else:
            self.emptyData = Text('NO AVAILABLE GAME DATA', self.font, 50, Color.WHITE, frame.rect.x + (100 if modeGame == 1 else 130), frame.rect.y + frame.rect.height/2)      
            self.emptyData.draw(self.screen)

# Allow individual execution file [Remove this when finished]
if __name__ == "__main__":
    diffGame = False
    game = Scoreboard(diffGame)
    game.run()


