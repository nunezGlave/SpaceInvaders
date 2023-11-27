from pygame import *
from Logical_Layer.Viewport.image_scale import ImageScale
from Logical_Layer.Viewport.screen_surface import Screen
from Logical_Layer.Util.limit import Limit
from Logical_Layer.Util.color import Color

class Enemy(sprite.Sprite):
    # Parameterized Constructor
    def __init__(self, gameScreen: Screen, scale: int, images: dict, img: ImageScale, row: int, column: int, totalRows: int):
        sprite.Sprite.__init__(self)
        self.screen = gameScreen.surface
        self.row = row
        self.column = column
        self.rows = totalRows
        self.dictImages = images
        self.images = []
        self.scale = self.load_images(scale, img)
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
        Limit.bordersCollision(self.rect, self.screen, Color.PURPLE1)
        self.screen.blit(self.image, self.rect)

    def load_images(self, scale: int, img: ImageScale):
        numberEnemy = {}
        enemyRowStruture = [['1_2', '1_1'],
                            ['2_2', '2_1'],
                            ['2_2', '2_1'], 
                            ['3_1', '3_2'],
                            ['3_1', '3_2']]
        
        #iRow = 0
        for row in range(self.rows):
            numberEnemy[row] = enemyRowStruture[row]
            #iRow += 0       
            #if iRow == len(enemyRowStruture) - 1:
            #    iRow = 0
    
        img1, img2  = (self.dictImages['enemy{}'.format(img_num)] for img_num in
                      numberEnemy[self.row])
        
        img1Scale = ImageScale(scale, img1, img.originalWidth, img.originalHeight, img.scaleFactor) 
        img2Scale = ImageScale(scale, img2,  img.originalWidth, img.originalHeight, img.scaleFactor)

        self.images.append(img1Scale.scaleImage)
        self.images.append(img2Scale.scaleImage)

        return img1Scale
    
