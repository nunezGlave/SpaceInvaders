from pygame import *
from Logical_Layer.Viewport.image_scale import ImageScale
from Logical_Layer.Viewport.screen_surface import Screen
from Logical_Layer.Util.collision import Collision
from Logical_Layer.Util.color import Color

class Ship(sprite.Sprite):
    # Parameterized Constructor
    def __init__(self, gameScreen: Screen, image: ImageScale):
        sprite.Sprite.__init__(self)
        self.screen = gameScreen.surface                                 # Screen where the content will be drawn
        self.image = image.scaleImage                                    # Scaled Image
        self.size = image.scaleSize                                      # Image's size
        self.xPos = gameScreen.halfWidth                                 # Middle position on the screen
        self.yPos = gameScreen.height - (self.size + 4)                  # Height position minus image size
        self.rect = self.image.get_rect(topleft=(self.xPos, self.yPos))
        self.speed = 5

    # Overrides the Update method which is responsible for displaying elements on the screen
    def update(self, keys, *args):
        col = Color()
        Collision.detectionBorders(self.rect, self.screen, col.YELLOW)
        self.screen.blit(self.image, self.rect)
