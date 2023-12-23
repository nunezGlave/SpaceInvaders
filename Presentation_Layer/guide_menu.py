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
    def __init__(self, difficulty: bool, modeGame: int):
        # Initialize super class
        super().__init__("Guide Menu")
        self.difficulty = difficulty
        self.modeGame = modeGame

        # Names of images
        singularImgs = ['mystery','enemy1_2', 'enemy2_2', 'enemy3_2', 'extra_button', 'difficulty_menu', 'guide_frame']
        sharedImgs = ['backspace', 'key_left', 'key_right', 'key_up', 'key_a', 'key_d', 'key_w']

        # Load images and font
        self.images = self.loadSingularImages(singularImgs, self.difficulty)
        self.shImages = self.loadSharedImages(sharedImgs)
        self.images =  self.images['basic'] if self.difficulty else self.images['doom']
        self.font = self.getFont()

        # Scale background image
        self.background = transform.scale(self.images['difficulty_menu'], (self.display.width, self.display.height))

        # Create guide menu's text
        self.frame =  Image(self.screen, self.images['guide_frame'], 1200, 750)
        self.title = Text('Game Information', self.font, 65, Color.WHITE, self.display.halfWidth, self.frame.rect.y + 55, Align.CENTER)      
   
        # Create guide menu's image
        self.enemy1 = Image(self.screen, self.images['enemy3_2'], 80, 68)
        self.enemy2 = Image(self.screen, self.images['enemy2_2'], 70, 66)
        self.enemy3 = Image(self.screen, self.images['enemy1_2'], 70, 66)
        self.enemy4 = Image(self.screen, self.images['mystery'], 110, 70)

        # Create guide buttons
        self.btnBack = Button(self.images['extra_button'], 0.4, 'Back', self.font)

    def handle_events(self, events) -> dict:
        for event in events:
            if event.type == KEYDOWN:
                if event.key == py.K_BACKSPACE:
                    print('entre')
                    return {'state': State.PLAYER, 'difficulty': self.difficulty}
            else:
                self.exit(event)

    def draw(self):
        # Draw background
        self.screen.blit(self.background, (0, 0))
        self.frame.draw(self.display.widthP(10), self.display.heightP(3))

        # Create Enemies' text
        heightSpace = 45
        self.subTitle1 = Text('Enemy Score', self.font, 55, Color.WHITE, (self.frame.rect.width//4) + 10, self.frame.rect.y + 180)      
        self.subTitle2 = Text('Game Controller', self.font, 55, Color.WHITE, (self.frame.rect.centerx) + 95, self.subTitle1.yPos)
        self.enemy1Text = Text('   =   10 pts', self.font, 45, Color.GREEN1, self.subTitle1.xPos + 100, self.subTitle1.heightPosY + heightSpace)                 
        self.enemy2Text = Text('   =  20 pts', self.font, 45, Color.BLUE1, self.enemy1Text.xPos , self.enemy1Text.heightPosY + heightSpace)                   
        self.enemy3Text = Text('   =  30 pts', self.font, 45, Color.PURPLE1, self.enemy2Text.xPos , self.enemy2Text.heightPosY + heightSpace)                  
        self.enemy4Text = Text('   =  ?????', self.font, 45, Color.RED1, self.enemy3Text.xPos ,self.enemy3Text.heightPosY + heightSpace)                      

        # Draw enemies' text
        self.title.draw(self.screen)
        self.subTitle1.draw(self.screen)
        self.subTitle2.draw(self.screen)
        self.enemy1Text.draw(self.screen)
        self.enemy2Text.draw(self.screen)
        self.enemy3Text.draw(self.screen)
        self.enemy4Text.draw(self.screen)

        # Draw enemies
        moveLeft = 70
        moveUp = 5
        self.enemy1.draw(self.enemy1Text.xPos - moveLeft - 6, self.enemy1Text.yPos - moveUp - 5)
        self.enemy2.draw(self.enemy1Text.xPos - moveLeft, self.enemy2Text.yPos - moveUp)
        self.enemy3.draw(self.enemy1Text.xPos - moveLeft, self.enemy3Text.yPos - moveUp)
        self.enemy4.draw(self.enemy1Text.xPos - moveLeft - 20, self.enemy4Text.yPos - moveUp + 5)

        # Draw guide depend on modeGame
        if self.modeGame == 1:
            # Create guide buttons
            self.keyUp1 = Image(self.screen, self.shImages['key_up'], 96, 96)
            self.keyleft1 = Image(self.screen, self.shImages['key_left'], 96, 96)
            self.keyRight1 = Image(self.screen, self.shImages['key_right'], 96, 96)

            # Create button images
            self.keyleft1.draw(self.subTitle2.xPos , self.subTitle2.heightPosY + 60)
            self.keyUp1.draw(self.subTitle2.xPos, self.keyleft1.rect.bottom)
            self.keyRight1.draw(self.subTitle2.xPos, self.keyUp1.rect.bottom)
            
            # Create description
            self.descLeft1 = Text('Move Left', self.font, 45, Color.WHITE, self.keyleft1.rect.right + 20, self.keyleft1.rect.y + 20)      
            self.descUp1 = Text('Shoot', self.font, 45, Color.WHITE, self.keyUp1.rect.right + 20, self.keyUp1.rect.y + 20)      
            self.descRight1 = Text('Move Right', self.font, 45, Color.WHITE, self.keyRight1.rect.right + 20, self.keyRight1.rect.y + 20)      
            
            # Draw description
            self.descLeft1.draw(self.screen)
            self.descUp1.draw(self.screen)
            self.descRight1.draw(self.screen)
        else:
            # Create players description
            self.descPl1 = Text('PLAYER-1', self.font, 45, Color.ORANGE, self.subTitle2.xPos - 5, self.subTitle2.heightPosY + 55)                          
            self.descPl1.rotate(90)

            # Create guide buttons
            self.keyUp1 = Image(self.screen, self.shImages['key_up'], 65, 65)
            self.keyleft1 = Image(self.screen, self.shImages['key_left'], 65, 65)
            self.keyRight1 = Image(self.screen, self.shImages['key_right'], 65, 65)            
            self.keyUp2 = Image(self.screen, self.shImages['key_w'], 65, 65)
            self.keyleft2 = Image(self.screen, self.shImages['key_a'], 65, 65)
            self.keyRight2 = Image(self.screen, self.shImages['key_d'], 65, 65) 

            # Create button images
            self.keyleft1.draw(self.descPl1.xPos + 70, self.subTitle2.heightPosY + 30)
            self.keyUp1.draw(self.keyleft1.rect.x, self.keyleft1.rect.bottom)
            self.keyRight1.draw(self.keyleft1.rect.x, self.keyUp1.rect.bottom)
            self.keyleft2.draw(self.keyRight1.rect.x , self.keyRight1.rect.bottom + 30)
            self.keyUp2.draw(self.keyleft2.rect.x, self.keyleft2.rect.bottom)
            self.keyRight2.draw(self.keyUp2.rect.x, self.keyUp2.rect.bottom)

            self.descPl2 = Text('PLAYER-2', self.font, 45, Color.ORANGE, self.subTitle2.xPos - 5, self.keyRight1.rect.bottom + 50)                          
            self.descPl2.rotate(90)

            # Create description
            heightDesc = 6
            widthDesc = 20
            self.descLeft1 = Text('Move Left', self.font, 45, Color.WHITE, self.keyleft1.rect.right + widthDesc, self.keyleft1.rect.y + heightDesc)      
            self.descUp1 = Text('Shoot', self.font, 45, Color.WHITE, self.keyUp1.rect.right + widthDesc, self.keyUp1.rect.y + heightDesc)      
            self.descRight1 = Text('Move Right', self.font, 45, Color.WHITE, self.keyRight1.rect.right + widthDesc, self.keyRight1.rect.y + heightDesc)      
            self.descLeft2 = Text('Move Left', self.font, 45, Color.WHITE, self.keyleft2.rect.right + widthDesc, self.keyleft2.rect.y + heightDesc)      
            self.descUp2 = Text('Shoot', self.font, 45, Color.WHITE, self.keyUp2.rect.right + widthDesc, self.keyUp2.rect.y + heightDesc)      
            self.descRight2 = Text('Move Right', self.font, 45, Color.WHITE, self.keyRight2.rect.right + widthDesc, self.keyRight2.rect.y + heightDesc)                          

            # Draw description
            self.descLeft1.draw(self.screen)
            self.descUp1.draw(self.screen)
            self.descRight1.draw(self.screen)
            self.descLeft2.draw(self.screen)
            self.descUp2.draw(self.screen)
            self.descRight2.draw(self.screen)
            self.descPl1.draw(self.screen)
            self.descPl2.draw(self.screen)

        # Draw button
        self.btnBack.drawIcon(self.screen, self.shImages['backspace'], self.display.widthP(75), self.display.heightP(92))

        # Capture button click
        # if self.btnBack.mouseClick():
        #     self.eventBackspace()

# Allow individual execution file [Remove this when finished]
if __name__ == "__main__":
    diffGame = False
    modeGame = 2
    game = GuideMenu(diffGame, modeGame)
    game.run()