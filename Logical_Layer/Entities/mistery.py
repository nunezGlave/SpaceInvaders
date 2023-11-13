from pygame import *
from Logical_Layer.Entities.enemies_group import EnemiesGroup
from Logical_Layer.Viewport.image_scale import ImageScale
from Logical_Layer.Viewport.screen_surface import Screen
from Logical_Layer.Util.limit import Limit
from Logical_Layer.Util.color import Color
from random import choice
import os

# Temporal
SOUND_PATH = os.getcwd() + '/Assets/Sounds/Doom/'

class Mystery(sprite.Sprite):
    # Parameterized Constructor
    def __init__(self, screenDimension: Screen, image : ImageScale, enemies: EnemiesGroup, positionX = 0, positionY = 0):
        sprite.Sprite.__init__(self)
        self.screenDimension = screenDimension  
        self.screen = self.screenDimension.surface    
        self.image = image.scaleImage
        self.rect = self.image.get_rect(topleft=(positionX, positionY))
        self.row = 5
        self.moveTime = 3000 
        self.startAnimation = self.moveTime + 1000
        self.collistionMystery = True
        self.direction = 1
        self.timer = time.get_ticks()
        self.mysteryEntered = mixer.Sound(SOUND_PATH + 'mysteryentered.wav')
        self.mysteryEntered.set_volume(0.3)
        self.playSound = True
        self.leftlimit = positionX - 20
        self.rightLimit = self.screenDimension.width + 40
        self.groupPosition = enemies

    # Overrides the Update method which is responsible for displaying elements on the screen
    def update(self, keys, currentTime, *args):
        Limit.bordersCollision(self.rect, self.screen, Color.TEAL)
        Limit.horizontalBorder(self.screenDimension, Color.BLUE, self.rect.bottom)
        resetTimer = False
        passed = currentTime - self.timer

        # Wait some seconds to display the ship
        if passed > self.moveTime:
            # Avoid the collision of the mystery ship with groups of enemies
            if self.collistionMystery:
                # Search the matrix of enemies for one enemy that is in the first row and alive
                for column in self.groupPosition._aliveColumns:
                    enemy = self.groupPosition.enemies[self.groupPosition._aliveRows[0]][column]
                    if enemy == None:
                        continue
                    else:
                        # Stop search when the enemies in the first row are below the mystery ship
                        if(enemy.rect.top > self.rect.bottom):
                            self.moveTime = self.startAnimation
                            self.collistionMystery = False
                        break
        
            # Permit the ship to navigate once it has been confirmed that there is no risk of collision with the enemy group
            if self.moveTime >= self.startAnimation:
                if (self.rect.x < 0 or self.rect.x > self.screenDimension.width) and self.playSound:
                    self.mysteryEntered.play()
                    self.playSound = False
                    self.moveTime = choice([12000, 15000, 20000, 25000])    # Select the duration for the ship to reappear

                if self.rect.x < self.rightLimit and self.direction == 1:
                    self.mysteryEntered.fadeout(4000)
                    self.rect.x += 2
                    self.screen.blit(self.image, self.rect)

                if self.rect.x > self.leftlimit and self.direction == -1:
                    self.mysteryEntered.fadeout(4000)
                    self.rect.x -= 2
                    self.screen.blit(self.image, self.rect)


        if self.rect.x > self.screenDimension.width + 30:
            self.playSound = True
            self.direction = -1
            resetTimer = True

        if self.rect.x < (self.leftlimit + 10):
            self.playSound = True
            self.direction = 1
            resetTimer = True

        if passed > self.moveTime and resetTimer:
            self.timer = currentTime
