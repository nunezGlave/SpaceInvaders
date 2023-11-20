from Logical_Layer.Viewport.screen_surface import Screen
from abc import ABC, abstractmethod
import pygame as py
import os, sys

class Viewport(ABC):
    def __init__(self, title):
        # Initialize pygame's variables
        py.init()
        
        # Get screen dimensions
        infoScreen = py.display.Info()
        displayMode = py.display.set_mode((infoScreen.current_w , infoScreen.current_h))

        # Assets' path
        mainPath = os.getcwd()
        fontPath = mainPath + '\\Assets\\Fonts'
        imgPath = mainPath + '\\Assets\\Images'

        # Create class' attributes
        self.title = title
        self.screen = displayMode
        self.display = Screen(displayMode)
        self.clock = py.time.Clock()
        self.fontPath = fontPath
        self.imagePath = imgPath

        # Set window's title
        py.display.set_caption(self.title)

        # Temp
        print('Display Mode of {}'.format(self.title))
        print('{} - {}'.format(self.display.width, self.display.height))

    # Event handling
    @abstractmethod
    def handle_events(self, events):
        pass

    @abstractmethod
    def draw(self):
        pass

    @classmethod
    def exit(self, event):
        if event.type == py.QUIT or (event.type == py.KEYUP and event.key == py.K_ESCAPE):
            sys.exit()

    def update(self):
        py.display.update()

    def run(self):
        # Run the game
        while True:
            self.handle_events(py.event.get())
            self.draw()
            self.update()
            self.clock.tick(60)

