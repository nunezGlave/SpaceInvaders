from pygame import *
from Logical_Layer.Players.a3c_observer import A3C_Observer
from Logical_Layer.Players.dqn_observer import DQN_Observer
from Logical_Layer.Players.human_observer import Human_Observer
from Logical_Layer.Viewport.screen_surface import Screen
from Logical_Layer.Viewport.image_scale import ImageScale
from Logical_Layer.Entities.ship import Ship
from Logical_Layer.Entities.bullet import Bullet
from Logical_Layer.Util.limit import Limit
from Logical_Layer.Util.color import Color

class Player(sprite.Sprite):
    # Parameterized Constructor
    def __init__(self, gameScreen: Screen, playerInfo: dict, imageShip: ImageScale, imageLaser: Surface, scoreLimit: int, coordinateX: int):
        sprite.Sprite.__init__(self)
        self.screen  = gameScreen
        self.id = playerInfo['id'] 
        self.name = playerInfo['name'] 
        self.type = playerInfo['typePlayer']
        self.imageShip = imageShip
        self.imageLaser = imageLaser
        self.scoreLimit = scoreLimit

        self.command_left = False
        self.command_right = False
        self.command_shoot = False

        self.ship = Ship(self.screen, self.imageShip, coordinateX)
        self.bullets = sprite.Group()
        self.controler = self.determineController(self.type)
        self.shipAlive = True
        self.reloadTimer = 1

    # Revive ship
    def renewShip(self, newPosX: float, newPosY: float):
        self.ship = Ship(self.screen, self.imageShip, newPosX, newPosY)
        self.shipAlive = True

    # Determine the type of player
    def determineController(self, type: int):
        match type:
            case 0:
                return Human_Observer(self, type)
            case 1:
                return Human_Observer(self, type)
            case 2:
                return A3C_Observer(self)
            case 3:
                return DQN_Observer(self)
            case _:
                return Human_Observer(self, 0)
            
    # Determine the types of player's movement
    def command(self, command):
        if command == "left":
            self.command_left = True
        elif command == "right":
            self.command_right = True
        elif command == "shoot":
            self.command_shoot = True

    # Evaluate the user's input
    def checkInput(self, score: int, sounds: dict):
        # Determine ship's limit
        leftLimit = 10
        rightLimit = self.screen.width - 10

        # Draw boundaries of the player's ship
        Limit.verticalBorders(self.screen, Color.PURPLE1, leftLimit, rightLimit)

        # Check movement to the left
        if self.command_left:
            if self.ship.rect.left > leftLimit:
                self.ship.rect.x -= self.ship.speed

            self.command_left = False

        # Evaluate movement to the right
        if self.command_right:
            if self.ship.rect.right < rightLimit: 
                self.ship.rect.x += self.ship.speed

            self.command_right = False

        # Evaluate single or double shot
        if self.command_shoot:
            if (time.get_ticks() - self.reloadTimer > 650) and self.shipAlive and len(self.bullets) == 0: 
                # Reduces firing rate
                self.reloadTimer = time.get_ticks()   

                # Evaluate the type of shoot
                if score < self.scoreLimit:
                    bullet = Bullet(self.screen, self.ship.rect.centerx, self.ship.rect.top - 9, -1, 15, self.imageLaser)
                    self.bullets.add(bullet)
                    sounds['shoot1'].play()
                else:
                    leftbullet = Bullet(self.screen, self.ship.rect.centerx - 15, self.ship.rect.top - 9, -1, 15, self.imageLaser)
                    rightbullet = Bullet(self.screen, self.ship.rect.centerx + 15, self.ship.rect.top - 9, -1, 15, self.imageLaser)
                    self.bullets.add(leftbullet, rightbullet)
                    sounds['shoot2'].play()

            self.command_shoot = False

    # Update bullets and controller
    def update(self, score: int, enemies: sprite.Group, enemyBullets: sprite.Group):
        self.bullets.update()
        self.controler.update(score, enemies, enemyBullets)


