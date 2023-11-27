from pygame import *
from Logical_Layer.Viewport.image_scale import ImageScale
from Logical_Layer.Viewport.screen_surface import Screen
from Logical_Layer.Util.limit import Limit
from Logical_Layer.Util.color import Color

class Ship(sprite.Sprite):
    # Parameterized Constructor
    def __init__(self, gameScreen: Screen, image: ImageScale, positionX = 0, positionY = 0):
        sprite.Sprite.__init__(self)                             # Initialize the superclass constructor
        self.screen = gameScreen.surface                         # Screen where the content will be drawn
        self.image = image.scaleImage                            # Scaled Image
        self.size = image.scaleWidth                             # Image's size
        self.speed = 5                                           # Speed of movement
        if positionX != 0:
            self.xPos = positionX                                # Specified x-axis position
        else:
            self.xPos = gameScreen.halfWidth - (self.size // 2)  # Default x-axis middle position

        if positionY != 0:
            self.yPos = positionY                                # Specified y-axis position
        else:
            self.yPos = gameScreen.height - (self.size + 4)      # Default y-axis position 

        # Set the position of the ship
        self.rect = self.image.get_rect(topleft=(self.xPos, self.yPos)) 

    # Overrides the update method of the Sprite class
    def update(self, keys, *args):
        Limit.bordersCollision(self.rect, self.screen, Color.YELLOW1)
        self.screen.blit(self.image, self.rect)                 # Display image on the screen

