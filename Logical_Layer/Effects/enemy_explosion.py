from pygame import *
from Logical_Layer.Viewport.image_scale import ImageScale
from Logical_Layer.Viewport.screen_surface import Screen
from Logical_Layer.Entities.enemy import Enemy

class EnemyExplosion(sprite.Sprite):
    # Parameterized Constructor
    def __init__(self, gameScreen: Screen, scale: int, enemy: Enemy, *groups):
        super(EnemyExplosion, self).__init__(*groups)
        self.screen = gameScreen.surface        
        self.listImages = enemy.dictImages
        self.image = ImageScale(scale, self.listImages[enemy.explosion], enemy.scale.originalWidth, enemy.scale.originalHeight)
        self.image2 = ImageScale(scale, self.listImages[enemy.explosion], enemy.scale.originalWidth, enemy.scale.originalHeight)
        self.image = self.image.scaleImage
        self.image2 = self.image2.scaleImage

        self.rect = self.image.get_rect(topleft=(enemy.rect.x, enemy.rect.y))
        self.timer = time.get_ticks()

    # Overrides the Update method which is responsible for displaying elements on the screen
    def update(self, current_time, *args):
        passed = current_time - self.timer
        if passed <= 100:
            self.screen.blit(self.image, self.rect)
        elif passed <= 200:
            self.screen.blit(self.image2, (self.rect.x - 6, self.rect.y - 6))
        elif 400 < passed:
            self.kill()
