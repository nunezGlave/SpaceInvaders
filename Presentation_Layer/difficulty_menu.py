# Allow individual execution file [Remove this when finished]
import os, sys
FULL_PATH = os.getcwd()
sys.path.append(FULL_PATH)

# Import libraries
from pygame import *
from Logical_Layer.Interfaces.viewport import Viewport
from Logical_Layer.Util.text import Text
from Logical_Layer.Util.color import Color as color
from Logical_Layer.Viewport.button import Button
from Logical_Layer.Viewport.image_scale import ImageScale

class DifficultyMenu(Viewport):
    def __init__(self):
        # Initialize super class
        super().__init__("Difficulty Menu")

        # Load imagenes and font
        self.invadersImgs = self.loadImages(True)
        self.doomImgs = self.loadImages(False)
        self.font = '{0}\\knight_warrior.otf'.format(self.fontPath)

        # Default images and statu's button
        self.images = self.invadersImgs
        self.stateBtn1 = self.images['button_active']
        self.stateBtn2 = self.images['button_inactive']
        self.dictInfo = self.createInfoDict()
        self.info = self.dictInfo['easy']
        
    def handle_events(self, events):
        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    self.changeState(True)
                elif event.key == K_DOWN:
                    self.changeState(False)
                elif event.key == K_BACKSPACE:
                    return 'switch_to_introduction'
                if event.key == K_RETURN:
                    print('Enter')      
            else:
                Viewport.exit(event)

    def draw(self):
        # Display background
        self.screen.blit(self.images['difficulty_menu'], (0, 0))

        # Create and display logo
        self.logo = ImageScale(1, self.images['logo'], 520, 230)
        self.logo.draw(self.screen, self.display.widthP(5), self.display.heightP(4))
        
        # Create buttons
        self.btn1 = Button(self.stateBtn1, self.logo.rect.x + 30, self.logo.rect.bottom + 40, 0.35)
        self.btn2 = Button(self.stateBtn2, self.logo.rect.x + 30, self.btn1.rect.bottom + 10, 0.35)

        self.btn3 = Button(self.images['extra_button'], self.display.widthP(78), self.display.heightP(92), 0.4)
        self.btn3.draw(self.screen)
        
        self.btn4 = Button(self.images['extra_button'], self.btn3.rect.right -15, self.btn3.rect.y, 0.4)
        self.btn4.draw(self.screen)

        # Create images
        self.enter = ImageScale(1, self.images['enter'], 50, 50)
        self.enter.draw(self.screen, self.btn4.rect.x + 20, self.btn4.rect.y + 2)

        self.backspace = ImageScale(1, self.images['backspace'], 40, 40)
        self.backspace.draw(self.screen, self.btn3.rect.x + 30, self.btn3.rect.y + 10)

        # Create buttons' text
        self.text1 = Text('EASY', self.font, 50, color.WHITE, self.btn1.x + self.btn1.xP(18), self.btn1.y + self.btn1.yP(25))      
        self.text2 = Text('HARD', self.font, 50, color.WHITE, self.btn2.x + self.btn2.xP(18), self.btn2.y + self.btn2.yP(25))     
        self.text3 = Text('Back', self.font, 30, color.WHITE, self.backspace.rect.right + 10, self.backspace.rect.y + 4)     
        self.text4 = Text('Enter', self.font, 30, color.WHITE, self.enter.rect.right + 5, self.enter.rect.y + 10)     

        # Create and draw frame
        self.frame = ImageScale(1, self.images['frame'], 450, 300)
        self.frame.draw(self.screen, self.btn2.x, self.btn2.rect.bottom + 20)

        # Create and display frame's information
        self.displayInfo(self.frame.rect.x + 40, self.frame.rect.y + 60)

        # Display buttons
        if self.btn1.draw(self.screen):
            self.changeState(True)

        if self.btn2.draw(self.screen):
            self.changeState(False)


        # Display texts
        self.text1.draw(self.screen)
        self.text2.draw(self.screen)
        self.text3.draw(self.screen)
        self.text4.draw(self.screen)

    def changeState(self, state: bool):
        if state:
           self.images = self.invadersImgs
           self.stateBtn1 = self.images['button_active']
           self.stateBtn2 = self.images['button_inactive']
           self.info = self.dictInfo['easy']
        else:
           self.images = self.doomImgs
           self.stateBtn1 = self.images['button_inactive']
           self.stateBtn2 = self.images['button_active']
           self.info = self.dictInfo['hard']

    def loadImages(self, folder: bool):
        # List of images' name
        nameImages = ['button_inactive','button_active', 'logo', 'difficulty_menu', 'frame', 'extra_button', 'backspace', 'enter']

        # Choose folder
        path = 'Basic' if folder else 'Doom'
        path = '{0}\\{1}'.format(self.imagePath, path)

        # Create dictionary of images
        result_dict = {}
        for name in nameImages:
            if name.find('menu') > -1:
                background = image.load('{0}\\{1}.png'.format(path, name)).convert()
                result_dict[name] = transform.scale(background, (self.display.width, self.display.height))
            else:
                result_dict[name] = image.load('{0}\\{1}.png'.format(path, name)).convert_alpha()

        return result_dict

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
        numbers = ['6', '4', '40', '10', '3', '2', '60', '20']
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