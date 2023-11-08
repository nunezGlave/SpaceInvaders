from pygame import *
from Logical_Layer.Viewport.screen_surface import Screen
from Logical_Layer.Entities.mistery import Mystery
from Logical_Layer.Util.color import Color
from Logical_Layer.Util.text import Text
import os

FULL_PATH = os.getcwd()
FONT_PATH = FULL_PATH + '/Assets/Fonts/'
FONT = FONT_PATH + 'space_invaders.ttf'

class MysteryExplosion(sprite.Sprite):
    # Parameterized Constructor
    def __init__(self, gameScreen: Screen, mystery : Mystery, score: int, *groups):
        super(MysteryExplosion, self).__init__(*groups)
        self.text = Text(str(score), FONT, 20, Color.WHITE, mystery.rect.x + 20, mystery.rect.y + 6) # Change this part
        self.timer = time.get_ticks()
        self.screen = gameScreen.surface

    # Overrides the Update method which is responsible for displaying elements on the screen
    def update(self, current_time, *args):
        passed = current_time - self.timer
        if passed <= 200 or 400 < passed <= 600:
            self.text.draw(self.screen)
        elif 600 < passed:
            self.kill()