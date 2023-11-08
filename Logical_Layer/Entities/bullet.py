from pygame import *
from Logical_Layer.Viewport.screen_surface import Screen
from Logical_Layer.Util.collision import Collision
from Logical_Layer.Util.color import Color

class Bullet(sprite.Sprite):
    # Parameterized Constructor
    def __init__(self, gameScreen: Screen, xPos: int, yPos: int, direction: int, speed: float, image: Surface, side: str):
        sprite.Sprite.__init__(self)
        self.game = gameScreen
        self.screen = gameScreen.surface
        self.image = image
        self.rect = self.image.get_rect(topleft=(xPos, yPos))
        self.direction = direction
        self.speed = speed
        self.side = side
   
    # Overrides the Update method which is responsible for displaying elements on the screen
    def update(self, keys, *args):
        Collision.detectionBorders(self.rect, self.screen, Color.BLUE)
        self.screen.blit(self.image, self.rect)
        self.rect.y += self.speed * self.direction
        if self.rect.y < 32 or self.rect.y > self.game.height:
            self.kill()
