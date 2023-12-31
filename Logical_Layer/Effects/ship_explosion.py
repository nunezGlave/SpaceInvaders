from pygame import *
from Logical_Layer.Entities.ship import Ship
from Logical_Layer.Viewport.screen_surface import Screen

class ShipExplosion(sprite.Sprite):
    # Parameterized Constructor
    def __init__(self, gameScreen: Screen, ship : Ship, *groups):
        super(ShipExplosion, self).__init__(*groups)
        self.screen = gameScreen.surface                                      
        self.image = ship.image
        self.timer = time.get_ticks()
        self.rect = self.image.get_rect(topleft=(ship.rect.x, ship.rect.y))   # Set the position of the explosion effect with the current position of the ship

    # Overrides the update method of the Sprite class
    def update(self, current_time, *args):
        passed = current_time - self.timer                                    # Used to create a momentary fading effect
        if 300 < passed <= 600:
            self.screen.blit(self.image, self.rect)                           
        elif 900 < passed:
            self.kill()
