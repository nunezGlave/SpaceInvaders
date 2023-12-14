# Allow individual execution file [Remove this when finished]
import os, sys
FULL_PATH = os.getcwd()
sys.path.append(FULL_PATH)

# Import libraries
from pygame import *
from Logical_Layer.Interfaces.viewport import Viewport
from Logical_Layer.Util.text import Text
from Logical_Layer.Util.color import Color as color
from Logical_Layer.Util.button import Button
from Logical_Layer.Util.state import State
from Logical_Layer.Viewport.image_scale import ImageScale
import pygame as py

class DifficultyMenu(Viewport):
    def __init__(self):
        # Initialize super class
        super().__init__("Difficulty Menu")
        self.gameDifficulty = True

        # List of images' names
        uniqueImgs = ['button_inactive','button_active', 'difficulty_menu', 'frame', 'extra_button', 'logo']
        sharedImgs = ['backspace', 'enter']
       
        # Load imagenes and font
        self.uniqImages = self.loadSharedImages(sharedImgs)
        self.reptImages = self.loadSingularImages(uniqueImgs)
        self.font = self.getFont()

        # Get difficulty info
        self.dictInfo = self.createInfoDict()

        # Default repeated images and unique images
        self.images = self.reptImages['basic']
        self.imgState1 = self.images['button_active']
        self.imgState2 = self.images['button_inactive']
        self.imgState3 = self.images['extra_button']
        self.imgBack = self.uniqImages['backspace']
        self.imgEnter = self.uniqImages['enter']
        self.info = self.dictInfo['easy']

    def handle_events(self, events) -> dict:
        for event in events:
            if event.type == KEYDOWN:
                match event.key:
                    case py.K_UP:
                        self.changeState(True)
                    case py.K_DOWN:
                        self.changeState(False)
                    case py.K_BACKSPACE:
                        return {'state': State.INTRO}
                    case py.K_RETURN:
                        return {'state': State.PLAYER, 'difficulty': self.gameDifficulty}
                    case _:
                        pass
            else:
                self.exit(event)

    def draw(self):
        # Display background
        background = transform.scale(self.images['difficulty_menu'], (self.display.width, self.display.height))
        self.screen.blit(background, (0, 0))
        sc = self.display

        # Create and display logo
        logo = ImageScale(1, self.images['logo'], 520, 230)
        logo.draw(self.screen, sc.widthP(5), sc.heightP(4))

        # Create buttons
        btnEasy = Button(self.imgState1, 0.35, 'EASY', self.font)
        btnHard = Button(self.imgState2, 0.35, 'HARD', self.font)
        btnBack = Button(self.imgState3, 0.4, 'Back', self.font)
        btnEnter = Button(self.imgState3, 0.4, 'Select', self.font)

        # Draw buttons
        btnEasy.draw(self.screen, logo.rect.left + 30, logo.rect.bottom + 40, 18, 24)
        btnHard.draw(self.screen, logo.rect.left + 30, btnEasy.rect.bottom + 10, 18, 24)
        btnBack.drawIcon(self.screen, self.imgBack, sc.widthP(78), sc.heightP(92))
        btnEnter.drawIcon(self.screen, self.imgEnter, btnBack.rect.right - 15, btnBack.rect.top)

        # Create and draw frame
        self.frame = ImageScale(1, self.images['frame'], 450, 300)
        self.frame.draw(self.screen, btnHard.rect.left, btnHard.rect.bottom + 20)

        # Create and display frame's information
        self.displayInfo(self.frame.rect.x + 40, self.frame.rect.y + 60)

        # Capture button click
        if btnEasy.mouseClick():
            self.changeState(True)

        if btnHard.mouseClick():
            self.changeState(False)

    def changeState(self, state: bool):
        if state:
           self.images = self.reptImages['basic']
           self.imgState1 = self.images['button_active']
           self.imgState2 = self.images['button_inactive']
           self.imgState3 = self.images['extra_button']
           self.info = self.dictInfo['easy']
        else:
           self.images = self.reptImages['doom']
           self.imgState1 = self.images['button_inactive']
           self.imgState2 = self.images['button_active']
           self.imgState3 = self.images['extra_button']
           self.info = self.dictInfo['hard']

        self.gameDifficulty = state

    def displayInfo(self, xPos: int, yPos: int):
        heightCoor = yPos
        listText = [] 
        for index, line in enumerate(self.info):
            listText.append(Text(line, self.font, 29, color.WHITE, xPos, heightCoor))  # Create text object
            text : Text = listText[index]                                              
            text.draw(self.screen)                                                     # Draw text object
            heightCoor = text.textHeight + 15                                          # Set next line position

    def createInfoDict(self):
        # Information list
        template = ['- Number of protection blocks: {}',
                    '- Number of lives: {}',
                    '- Number of enemies: {}',
                    '- Enemy speed: {}']
        # Changing parts
        numbers = ['6', '3', '40', '15', '3', '2', '60', '20']
        countList = len(numbers) // 2
        
        # Dictionary and list temp
        info = {}
        list1, list2 = [], []

        # Create a dictionary based on the template and the numbers
        for index, number in enumerate(numbers):
            if index < countList:
                list1.append(template[index].format(number))
                info['easy'] = list1
            else:
                list2.append(template[index - countList].format(number))
                info['hard'] = list2

        return info
    
# Allow individual execution file [Remove this when finished]
if __name__ == "__main__":
    game = DifficultyMenu()
    game.run()