# Allow individual execution file [Remove this when finished]
import os, sys
FULL_PATH = os.getcwd()
sys.path.append(FULL_PATH)

# Import libraries
from pygame import *
from Logical_Layer.Interfaces.viewport import Viewport
from Logical_Layer.Util.text import Text
from Logical_Layer.Util.color import Color as color
from Logical_Layer.Util.align import Align
from Logical_Layer.Util.state import State

class IntroductionMenu(Viewport):
    def __init__(self):
        # Initialize super class
        super().__init__("Space Invaders Menu")
        
        # Load images an font
        images = self.loadSharedImages(['intro_menu'])
        self.font = self.getFont()

        # Set background image
        self.logo = images['intro_menu']
        self.background = transform.scale(self.logo, (self.display.width, self.display.height))

        # Create text messages
        self.optionMenu = Text('PRESS ENTER', self.font, 60, color.WHITE, self.display.widthP(48), self.display.heightP(91), Align.CENTER)      
        
        # Effect controllers
        self.timer = time.get_ticks()
        self.effectText = True

    def handle_events(self, events) -> dict:
        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    return {'state': State.DIFFICULTY}
            else:
                self.exit(event)

    def draw(self):
        # Display background
        self.screen.blit(self.background, (0, 0))

        # Calculate elapsed time
        elapsed_time = time.get_ticks() - self.timer 

        # Change optionMenu effect after 0.8 secondss
        if elapsed_time >= 800:
            self.timer  = time.get_ticks() 
            self.effectText =  not self.effectText

        # Display the optionMenu
        if self.effectText:
            self.optionMenu.draw(self.screen)

# Allow individual execution file [Remove this when finished]
if __name__ == "__main__":
    game = IntroductionMenu()
    game.run()