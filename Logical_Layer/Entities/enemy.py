from pygame import *
from Logical_Layer.Viewport.image_scale import ImageScale
from Logical_Layer.Viewport.screen_surface import Screen
from Logical_Layer.Util.collision import Collision
from Logical_Layer.Util.color import Color

class Enemy(sprite.Sprite):
    # Parameterized Constructor
    def __init__(self, gameScreen: Screen, image: ImageScale, row: int, column: int):
        sprite.Sprite.__init__(self)
        self.screen = gameScreen.surface
        self.size = image.scaleSize
        self.row = row
        self.column = column
        self.listImages = image.originalImage
        self.images = []
        self.load_images()
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()

    # It creates an animation effect by cycling through a sequence of images
    def toggle_image(self):
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]

    # Overrides the Update method which is responsible for displaying elements on the screen
    def update(self, *args):
        Collision.detectionBorders(self.rect, self.screen, Color.PURPLE)
        self.screen.blit(self.image, self.rect)

    def load_images(self):
        numberEnemy = {0: ['1_2', '1_1'],
                       1: ['2_2', '2_1'],
                       2: ['2_2', '2_1'],
                       3: ['3_1', '3_2'],
                       4: ['3_1', '3_2'],
                      }
        img1, img2 = (self.listImages['enemy{}'.format(img_num)] for img_num in
                      numberEnemy[self.row])
        self.images.append(ImageScale.scale(img1, self.size, self.size - 5))
        self.images.append(ImageScale.scale(img2, self.size, self.size - 5))
    
