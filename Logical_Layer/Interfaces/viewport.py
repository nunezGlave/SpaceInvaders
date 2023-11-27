from Logical_Layer.Viewport.screen_surface import Screen
from abc import ABC, abstractmethod
import pygame as py
import os, sys

class Viewport(ABC):
    def __init__(self, title : str, width : float = 0, height : float = 0, leftPos : int = 0, topPos : int = 0):
        # Initialize pygame's variables
        py.init()
        
        # Get screen dimensions
        infoScreen = py.display.Info()
        displayMode = py.display.set_mode((infoScreen.current_w , infoScreen.current_h))

        # Assets' path
        mainPath = os.getcwd()
        fontPath = mainPath + '\\Assets\\Fonts'
        imgPath = mainPath + '\\Assets\\Images'
        soundPath = mainPath + '\\Assets\\Sounds'

        # Create class' attributes
        self.title = title
        self.screen = displayMode
        self.display = Screen(displayMode)
        self.screenSub = self.screen.subsurface(py.Rect(leftPos, topPos, width, height))
        self.displaySub = Screen(self.screenSub)
        self.clock = py.time.Clock()
        self.fontPath = fontPath
        self.imagePath = imgPath
        self.sndPath = soundPath

        # Set window's title
        py.display.set_caption(self.title)

        # Temp
        print('Display Mode of {}'.format(self.title))
        print('{} - {}'.format(self.display.width, self.display.height))

    # Event handling
    @abstractmethod
    def handle_events(self, events):
        pass

    # Drawing
    @abstractmethod
    def draw(self):
        pass

    # Update content
    def update(self):
        py.display.update()

    # Execute game
    def run(self):
        # Run the game
        while True:
            self.handle_events(py.event.get())
            self.draw()
            self.update()
            self.clock.tick(60)

    # Load images
    def loadSingularImages(self, nameImages: list, uniqueFolder: bool = None):
        # Create dictionary of images
        outerDict = {}
        innerDict = {}

        # Images' folders
        folders = ['Basic', 'Doom'] if uniqueFolder == None else ['Basic'] if uniqueFolder else ['Doom'] 

        for folder in folders:
            # Choose path
            path = '{0}\\{1}'.format(self.imagePath, folder)

            # Traverse images' name
            for imageName in nameImages:
                # Parts of filename
                name, extension = os.path.splitext(imageName)

                # Create inner dict
                innerDict[name] = py.image.load('{0}\\{1}{2}'.format(path, name, extension if bool(extension) else '.png')).convert_alpha()
                
            # Asign inner dict to outer dict
            outerDict[folder.lower()]  = innerDict.copy()

            # Empty the dictionary
            innerDict.clear()

        return outerDict       

    def loadSharedImages(self, nameImages: list):
        # Create dictionary of images
        innerDict = {}
       
        # Path
        path = '{0}\\{1}\\'.format(self.imagePath, 'Shared')

        # Traverse images' name
        for imageName in nameImages:
            # Parts of filename
            name, extension = os.path.splitext(imageName)

            # Create inner dict                
            innerDict[name] = py.image.load('{0}\\{1}{2}'.format(path, name, extension if bool(extension) else '.png')).convert_alpha()
            
        return innerDict

    # Get specific font type
    def getFont(self, chosenFont: str = ''):
        match chosenFont:
            case 'space':
                nameFont = 'space_invaders.ttf'
            case _:
                nameFont = 'knight_warrior.otf'

        return  self.fontPath + '\\' + nameFont
    
    # Get sounds
    def getSoundPath(self, difficulty : bool):
        return  '{0}\\{1}\\'.format(self.sndPath, 'Basic' if difficulty else 'Doom')
    
    # Exit game
    @classmethod
    def exit(self, event):
        if event.type == py.QUIT or (event.type == py.KEYUP and event.key == py.K_ESCAPE):
            sys.exit()
