from pygame import *
from Logical_Layer.Viewport.image_scale import ImageScale
from Logical_Layer.Viewport.screen_surface import Screen
from Logical_Layer.Util.collision import Collision
from Logical_Layer.Util.color import Color

class Life(sprite.Sprite):
    # Parameterized Constructor
    def __init__(self, gameScreen: Screen, image: ImageScale, xPos: int, yPos: int):
        sprite.Sprite.__init__(self)
        self.screen = gameScreen.surface
        self.image = image.scaleImage
        self.size = image.scaleSize
        self.rect = self.image.get_rect(topleft=(xPos, yPos))
        self.posX =  xPos
        self.posY = yPos

    def update(self, *args):
        col = Color()
        Collision.detectionBorders(self.rect, self.screen, col.ORANGE)
        self.screen.blit(self.image, self.rect)
