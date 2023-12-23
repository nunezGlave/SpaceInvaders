from pygame import *
from Logical_Layer.Viewport.screen_surface import Screen
from Logical_Layer.Viewport.image_scale import ImageScale
from Logical_Layer.Entities.life import Life
from Logical_Layer.Entities.player import Player

class playersGroup(sprite.Group):
    # Parameterized Constructor
    def __init__(self, gameScreen: Screen, imageShips: list, imageLife: ImageScale, numberLives: int, lifePosX: float, lifePosY: float):
        sprite.Group.__init__(self)
        self.screen  = gameScreen
        self.createShipImgs(imageShips)
        self.imageLife = imageLife
        self._numLives = numberLives
        self.lifeX = lifePosX
        self.lifeY = lifePosY
        self.scoreLimit = 100
        self.score = 0
        self.typeShoot = True
        self.lives = []

        self.renewLives()

    # Reset lives
    def renewLives(self):
        if len(self.lives) == 0:
            self.lives = self._createLives()

    # Create lives
    def _createLives(self) -> sprite.Group:
        lives = []
        
        for num in range(self._numLives):
            if num == 0:
                firstLife = Life(self.screen, self.imageLife, self.lifeX, self.lifeY)
                lives.append(firstLife)
            else: 
                nextLife = Life(self.screen, self.imageLife, lives[num - 1].posX - self.imageLife.scaleWidth - 8, lives[num - 1].posY)
                lives.append(nextLife)

        return sprite.Group(lives)
    
    # Remove a life
    def removeLife(self) -> int:
        # Remove a life
        life : sprite.Sprite
        for index, life in enumerate(self.lives):
            if life.alive() and index == 0:
                life.kill() 

        # Restore score and type shoot
        self.score = 0
        self.typeShoot = True

        # Restore basic ship's image
        player : Player
        for player in self:
            player.ship.toggleImage(self.oneCannon)

        return len(self.lives)    

    # Improves the type of shot according to the score earned
    def improveShoots(self, score: int):
        self.score += score

    # Create the two types of images for the ship
    def createShipImgs(self, images: list):
        img1 : ImageScale = images[0]
        img2 : ImageScale = images[1]

        self.oneCannon = img1.newImage()
        self.doubleCannon = img2.newImage()

    # Update the image of each player with a ship to two cannons
    def upgradeShip(self) -> bool:
        if self.score >= self.scoreLimit and self.typeShoot:
            player : Player
            for player in self:
                player.ship.toggleImage(self.doubleCannon)
            
            self.typeShoot = False

    # Group bullets from each player
    @property
    def bullets(self):
        groupBullets = sprite.Group()
        player : Player

        for player in self:
            groupBullets.add(player.bullets)

        return groupBullets

    # Group ships from each player
    @property
    def ships(self):
        groupShip = sprite.Group()
        player : Player

        for player in self:
            groupShip.add(player.ship)   

        return groupShip     
        
    # Update players
    def update(self, score: int, enemies: sprite.Group, enemyBullets: sprite.Group):
        # Update lives 
        self.lives.update()

        # Update players
        player : Player
        for player in self:
            player.update(score, enemies, enemyBullets)
