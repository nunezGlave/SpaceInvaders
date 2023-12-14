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

    # Load the two possible images
    def load_images(self, scale: int, img: ImageScale):
        posEnemy = {}
        enemyRowStruture = self.getEnemiesRow()
        
        for row in range(self.rows):
            posEnemy[row] = enemyRowStruture[row]

        img1, img2  = (self.dictImages[img_name] for img_name in posEnemy[self.row])

        img1Scale = ImageScale(scale, img1, img.originalWidth, img.originalHeight, img.scaleFactor) 
        img2Scale = ImageScale(scale, img2,  img.originalWidth, img.originalHeight, img.scaleFactor)

        self.images.append(img1Scale.scaleImage)
        self.images.append(img2Scale.scaleImage)

        self.explosion, self.score = self.getConnectedValues(posEnemy)
        return img1Scale
    
    # Get the list of enemy names for each row
    def getEnemiesRow(self):
        enemies = []
        rows = self.rows
        typeEnemy = 3
        iteEnemy = typeEnemy

        for nRow in range(rows):
            if nRow < typeEnemy:
                num = nRow + 1
                enemies.append(['enemy{0}_2'.format(num), 'enemy{0}_1'.format(num)])
            else:
                enemies.append(['enemy{0}_2'.format(iteEnemy), 'enemy{0}_1'.format(iteEnemy)])
                iteEnemy -= 1
                if iteEnemy == 0:
                    iteEnemy = 3
        
        enemies.sort()

        return enemies
    
    # Get enemy's explosion and score.
    def getConnectedValues(self, enemies: str):
        imgName = enemies[self.row][0]
        imgName = imgName[:6]
        if imgName == 'enemy1':
            return ['explosion_purple', 30]
        elif imgName == 'enemy2':
            return ['explosion_blue', 20]
        elif imgName == 'enemy3':
            return ['explosion_green', 10]
