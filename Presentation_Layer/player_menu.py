# Allow individual execution file [Remove this when finished]
import os, sys
FULL_PATH = os.getcwd()
sys.path.append(FULL_PATH)

# Import libraries
from pygame import *
from Logical_Layer.Interfaces.viewport import Viewport
from Logical_Layer.Util.state import State
from Logical_Layer.Util.button import Button
from Logical_Layer.Util.image import Image
from Logical_Layer.Util.color import Color
import pygame as py

class PlayerMenu(Viewport):
    def __init__(self, difficulty: bool):
        # Initialize super class
        super().__init__("Difficulty Menu")    

        # Validate difficulty    
        self.difficulty = difficulty if isinstance(difficulty, bool) else True

        # Names of images
        uniqueImgs = ['difficulty_menu', 'button_active', 'button_inactive', 'frame_group', 'logo', 'extra_button', 'life']
        sharedImgs = ['backspace', 'enter', 'left_arrow', 'right_arrow']

        # Names of players
        self.playerName = ['PL1', 'PL2', 'A3C', 'DQN']

        # Load images and font
        self.unImages = self.loadSingularImages(uniqueImgs, self.difficulty)
        self.shImages = self.loadSharedImages(sharedImgs)
        self.font = self.getFont()

        # Set default images
        self.unImages =  self.unImages['basic'] if self.difficulty else self.unImages['doom']
        self.active = self.unImages['button_active']
        self.inactive = self.unImages['button_inactive']
        self.imgPlayer = self.unImages['life']
        self.left = self.shImages['left_arrow']
        self.right = self.shImages['right_arrow']
        self.btnStates = [self.active, self.inactive, self.inactive]

        # Default multi-player elements
        self.showLeftArrow = [True, True, True, True] 
        self.showRigthArrow = [True, True, True, True] 
        self.playerIndex = [1, 1, 1, 1]
        self.stateIndex = 0
        self.team1 = []
        self.team2 = []

        # Scale background image
        self.background = transform.scale(self.unImages['difficulty_menu'], (self.display.width, self.display.height))

    def handle_events(self, events) -> dict:
        for event in events:
            if event.type == KEYDOWN:
                match event.key:
                    case py.K_UP:
                        if self.stateIndex > 0:
                            self.stateIndex -= 1
                            self.changeState()
                    case py.K_DOWN:
                        if self.stateIndex < len(self.btnStates) - 1:
                            self.stateIndex += 1
                            self.changeState()
                    case py.K_BACKSPACE:
                        return {'state': State.DIFFICULTY}
                    case py.K_RETURN:
                        if self.stateIndex == 0:
                            return {'mode-game': 1, 'difficulty': self.difficulty, 'state': State.GAME, 
                                    'player': { 'typePlayer': 0, 'name': self.playerName[0]}}
                        elif self.stateIndex == 1:
                            if len(self.team1) == 1 and len(self.team2) == 1:
                                return {'mode-game': 2, 'difficulty' : self.difficulty, 'state': State.GAME,
                                        'player1': {'typePlayer': self.typePlayer(self.team1[0]), 'name': self.team1[0]},
                                        'player2': {'typePlayer': self.typePlayer(self.team2[0]), 'name': self.team2[0]}}
                        else:
                            return {'state': State.SCORE, 'difficulty': self.difficulty}
                    case _:
                        pass
            else:
                self.exit(event)

    def typePlayer(self, name: str):
        if name == self.playerName[0]:
            return 0
        elif name == self.playerName[1]:
            return 1
        elif name == self.playerName[2]:
            return 2
        else:
            return 3

    def draw(self):
        # Draw background
        self.screen.blit(self.background, (0, 0))
        sc = self.display

        # Create and display logo
        logo = Image(self.screen, self.unImages['logo'], 490, 200)
        logo.draw(sc.widthP(5), sc.heightP(4))

        # Create buttons
        btnSPlayer = Button(self.btnStates[0], 0.4, 'Single-Player', self.font)
        btnMPlayer = Button(self.btnStates[1], 0.4, 'Multi-Player', self.font)
        btnBoard = Button(self.btnStates[2], 0.4, 'Scoreboard', self.font, 0.55)

        # Draw buttons
        btnSPlayer.draw(self.screen, logo.rect.left + 30, logo.rect.bottom + 40, 18, 35)
        btnMPlayer.draw(self.screen, logo.rect.left + 30, btnSPlayer.rect.bottom + 15, 18, 35)
        btnBoard.draw(self.screen, logo.rect.left + 30, btnMPlayer.rect.bottom + 15, 18, 35)

        # Display multi-player menu
        if self.stateIndex == 1:
            # Create frames
            self.btnFrame1 = Button(self.unImages['frame_group'], 0.86, 'Team ({}/2)'.format(len(self.team1)), self.font, 0.3)
            self.btnFrame1.draw(self.screen, sc.widthP(38), btnSPlayer.rect.y, 11, 2)

            self.btnFrame2 = Button(self.unImages['frame_group'], 0.86, 'Team ({}/2)'.format(len(self.team2)), self.font, 0.3)
            self.btnFrame2.flip(True, False)
            self.btnFrame2.draw(self.screen, self.btnFrame1.rect.right + 180, btnSPlayer.rect.y, 55, 2)

            # Create list of positions
            self.playerPosX = [self.btnFrame1.rect.centerx, 
                               self.btnFrame1.rect.right + ((self.btnFrame2.rect.x - self.btnFrame1.rect.right) // 2), 
                               self.btnFrame2.rect.centerx]

            player1 = Image(self.screen, self.imgPlayer, 45)
            index1 = self.playerIndex[0]
            player1.drawCircle(self.playerPosX[index1], self.btnFrame1.rect.top + 95, Color.TEAL, Color.BLACK)
            player1.drawBox(self.playerName[0], self.font, self.left, self.right, self.showLeftArrow[0], self.showRigthArrow[0])
            self.detectArrow(player1, 0)

            player2 = Image(self.screen, self.imgPlayer, 45)
            index2 = self.playerIndex[1]
            player2.drawCircle(self.playerPosX[index2], player1.textRect.bottom + 50 , Color.GREEN2, Color.BLACK)
            player2.drawBox(self.playerName[1], self.font, self.left, self.right, self.showLeftArrow[1], self.showRigthArrow[1])
            self.detectArrow(player2, 1)

            player3 = Image(self.screen, self.imgPlayer, 45)
            index3 = self.playerIndex[2]
            player3.drawCircle(self.playerPosX[index3], player2.textRect.bottom + 50 , Color.PURPLE2, Color.BLACK)
            player3.drawBox(self.playerName[2], self.font, self.left, self.right, self.showLeftArrow[2], self.showRigthArrow[2])
            self.detectArrow(player3, 2)
        
            player4 = Image(self.screen, self.imgPlayer, 45)
            index4 = self.playerIndex[3]
            player4.drawCircle(self.playerPosX[index4], player3.textRect.bottom + 50 , Color.PINK1, Color.BLACK)
            player4.drawBox(self.playerName[3], self.font, self.left, self.right, self.showLeftArrow[3], self.showRigthArrow[3])
            self.detectArrow(player4, 3)

        # Create guide buttons
        btnBack = Button(self.unImages['extra_button'], 0.4, 'Back', self.font)
        btnEnter = Button(self.unImages['extra_button'], 0.4, 'Play' if self.stateIndex == 0 or self.stateIndex == 1 else 'View', self.font)

        # Draw guide buttons
        btnBack.drawIcon(self.screen, self.shImages['backspace'], sc.widthP(78), sc.heightP(92))
        btnEnter.drawIcon(self.screen, self.shImages['enter'], btnBack.rect.right - 15, btnBack.rect.top)

        # Capture button click
        if btnSPlayer.mouseClick():
            self.stateIndex = 0
            self.changeState()

        if btnMPlayer.mouseClick():
            self.stateIndex = 1
            self.changeState()

        if btnBoard.mouseClick():
            self.stateIndex = 2
            self.changeState()

    def changeState(self):
        for index in range(len(self.btnStates)):
            self.btnStates[index] = self.active if index == self.stateIndex else self.inactive

    def detectArrow(self, player: Image, index : int):
        # Detect arrows' click
        eventArrow = player.sidesClick() 

        # Move image to left, add image to list team1, and hide arrow 
        if eventArrow == 'LEFT' and self.playerIndex[index] > 0:
            #print('player - left', player.name)
            if self.playerIndex[index] == 1 and len(self.team1) < 2:
                self.team1.append(player.name)
                self.playerIndex[index] -= 1
                self.showLeftArrow[index] = False

            if self.playerIndex[index] == 2:
                if player.name in self.team1 : self.team1.remove(player.name)
                if player.name in self.team2 : self.team2.remove(player.name)
                self.playerIndex[index] -= 1
                self.showRigthArrow[index] = True

        # Move image to right, add image to list team2, and hide arrow 
        if eventArrow == 'RIGHT' and self.playerIndex[index] < len(self.playerPosX) - 1:
            #print('player - right', player.name)
            if self.playerIndex[index] == 1 and len(self.team2) < 2:
                self.team2.append(player.name)
                self.playerIndex[index] += 1  
                self.showRigthArrow[index] = False

            if self.playerIndex[index] == 0:
                if player.name in self.team1 : self.team1.remove(player.name)
                if player.name in self.team2 : self.team2.remove(player.name)
                self.playerIndex[index] += 1
                self.showLeftArrow[index] = True
  

# Allow individual execution file [Remove this when finished]
if __name__ == "__main__":
    diffGame = False
    game = PlayerMenu(diffGame)
    game.run()