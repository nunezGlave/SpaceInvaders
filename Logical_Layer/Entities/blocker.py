from pygame import *
from Logical_Layer.Viewport.screen_surface import Screen
from Logical_Layer.Util.collision import Collision
from Logical_Layer.Util.color import Color

class Blocker(sprite.Sprite):
    # Parameterized Constructor
    def __init__(self, gameScreen: Screen, size: int, color: tuple, row: int, column: int):
        sprite.Sprite.__init__(self)
        self.screen = gameScreen.surface
        self.height = size
        self.width = size
        self.color = color
        self.image = Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.row = row
        self.column = column

    # Overrides the Update method which is responsible for displaying elements on the screen
    def update(self, keys, *args):
        col = Color()
        Collision.detectionBorders(self.rect, self.screen, col.WHITE)
        self.screen.blit(self.image, self.rect)
