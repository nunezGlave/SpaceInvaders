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

class IntroductionMenu(Viewport):
    def __init__(self):
        super().__init__("Space Invaders Menu")
        self.logo = image.load(self.imagePath + '\\' + 'logo.jpg').convert()
        self.background = transform.scale(self.logo, (self.display.width, self.display.height))
        self.font = self.fontPath + '\\' + 'knight_warrior.otf' # 'knight_warrior.otf'
        self.optionMenu = Text('PRESS ENTER', self.font, 60, color.WHITE, self.display.widthP(48), self.display.heightP(91), Align.CENTER)      
        self.timer = time.get_ticks()
        self.effectText = True

    def handle_events(self, events):
        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    return 'switch_to_difficulty'
            else:
                Viewport.exit(event)

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