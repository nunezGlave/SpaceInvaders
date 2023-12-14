# Allow individual execution file [Remove this when finished]
import os, sys
FULL_PATH = os.getcwd()
sys.path.append(FULL_PATH)

# Import libraries
from pygame import *
from Logical_Layer.Interfaces.viewport import Viewport
from Logical_Layer.Util.text import Text
from Logical_Layer.Util.color import Color
from Logical_Layer.Util.align import Align
from Logical_Layer.Util.state import State
from Logical_Layer.Util.button import Button
from Logical_Layer.Util.image import Image
import pygame as py

class GuideMenu(Viewport):
    def __init__(self, difficulty: bool):
        # Initialize super class
        super().__init__("Guide Menu")
        self.difficulty = difficulty

        # Names of images
        singularImgs = ['mystery','enemy1_2', 'enemy2_2', 'enemy3_2', 'extra_button', 'difficulty_menu']
        sharedImgs = ['backspace']

        # Load images and font
        self.images = self.loadSingularImages(singularImgs, self.difficulty)
        self.shImages = self.loadSharedImages(sharedImgs)
        self.images =  self.images['basic'] if self.difficulty else self.images['doom']
        self.font = self.getFont()

        # Scale background image
        self.background = transform.scale(self.images['difficulty_menu'], (self.display.width, self.display.height))

        # Create guide menu's text
        titleMenu = 'Space Invader' if self.difficulty else 'Doom Invader'
        heightSpace = 40
        self.titleText = Text(titleMenu, self.font, 70, Color.WHITE, self.display.halfWidth, self.display.heightP(20), Align.CENTER)      
        self.enemy1Text = Text('   =   10 pts', self.font, 40, Color.GREEN1, self.display.halfWidth, self.titleText.textHeight + heightSpace)                 
        self.enemy2Text = Text('   =  20 pts', self.font, 40, Color.BLUE1, self.enemy1Text.xPos , self.enemy1Text.textHeight + heightSpace)                   
        self.enemy3Text = Text('   =  30 pts', self.font, 40, Color.PURPLE1, self.enemy2Text.xPos , self.enemy2Text.textHeight + heightSpace)                  
        self.enemy4Text = Text('   =  ?????', self.font, 40, Color.RED1, self.enemy3Text.xPos ,self.enemy3Text.textHeight + heightSpace)                      

        # Create guide menu's image
        self.enemy1 = Image(self.screen, self.images['enemy3_2'], 75, 62)
        self.enemy2 = Image(self.screen, self.images['enemy2_2'], 60, 56)
        self.enemy3 = Image(self.screen, self.images['enemy1_2'], 60, 56)
        self.enemy4 = Image(self.screen, self.images['mystery'], 100, 60)

        # Create guide buttons
        self.btnBack = Button(self.images['extra_button'], 0.4, 'Back', self.font)

    def handle_events(self, events) -> dict:
        for event in events:
            if event.type == KEYDOWN:
                if event.key == py.K_BACKSPACE:
                    return {'state': State.PLAYER, 'difficulty': self.difficulty}
            else:
                self.exit(event)

    def draw(self):
        # Draw background
        self.screen.blit(self.background, (0, 0))

        # Draw text
        self.titleText.draw(self.screen)
        self.enemy1Text.draw(self.screen)
        self.enemy2Text.draw(self.screen)
        self.enemy3Text.draw(self.screen)
        self.enemy4Text.draw(self.screen)

        # Draw images
        moveLeft = 70
        moveUp = 5

        self.enemy1.draw(self.enemy1Text.xPos - moveLeft - 6, self.enemy1Text.yPos - moveUp - 5)
        self.enemy2.draw(self.enemy1Text.xPos - moveLeft, self.enemy2Text.yPos - moveUp)
        self.enemy3.draw(self.enemy1Text.xPos - moveLeft, self.enemy3Text.yPos - moveUp)
        self.enemy4.draw(self.enemy1Text.xPos - moveLeft - 20, self.enemy4Text.yPos - moveUp + 5)
        
        # Draw button
        self.btnBack.drawIcon(self.screen, self.shImages['backspace'], self.display.widthP(78), self.display.heightP(92))

# Allow individual execution file [Remove this when finished]
if __name__ == "__main__":
    diffGame = False
    game = GuideMenu(diffGame)
    game.run()