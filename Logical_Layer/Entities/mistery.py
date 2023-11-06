from pygame import *
from Logical_Layer.Viewport.image_scale import ImageScale
from Logical_Layer.Viewport.screen_surface import Screen
from Logical_Layer.Util.collision import Collision
from Logical_Layer.Util.color import Color
import os

# Temporal
SOUND_PATH = os.getcwd() + '/Assets/Sounds/Doom/'

class Mystery(sprite.Sprite):
    # Parameterized Constructor
    def __init__(self, gameScreen: Screen, image : ImageScale):
        sprite.Sprite.__init__(self)
        self.game = gameScreen  
        self.screen = self.game.surface    
        self.image = ImageScale.scale(image.originalImage['mystery'], image.scaleSize, image.scaleSize - 25)
        self.rect = self.image.get_rect(topleft=(-80, 45))
        self.row = 5
        self.moveTime = 25000
        self.direction = 1
        self.timer = time.get_ticks()
        self.mysteryEntered = mixer.Sound(SOUND_PATH + 'mysteryentered.wav')
        self.mysteryEntered.set_volume(0.3)
        self.playSound = True

    # Overrides the Update method which is responsible for displaying elements on the screen
    def update(self, keys, currentTime, *args):
        col = Color()
        Collision.detectionBorders(self.rect, self.screen, col.TEAL)
        resetTimer = False
        passed = currentTime - self.timer
        if passed > self.moveTime:
            if (self.rect.x < 0 or self.rect.x > self.game.width) and self.playSound:
                self.mysteryEntered.play()
                self.playSound = False
            if self.rect.x < (self.game.width + 40) and self.direction == 1:
                self.mysteryEntered.fadeout(4000)
                self.rect.x += 2
                self.screen.blit(self.image, self.rect)
            if self.rect.x > -100 and self.direction == -1:
                self.mysteryEntered.fadeout(4000)
                self.rect.x -= 2
                self.screen.blit(self.image, self.rect)
       
        if self.rect.x > self.game.width + 30:
            self.playSound = True
            self.direction = -1
            resetTimer = True
        if self.rect.x < -90:
            self.playSound = True
            self.direction = 1
            resetTimer = True
        if passed > self.moveTime and resetTimer:
            self.timer = currentTime
