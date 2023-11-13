''' SPACE INVADERS
    Created by Lee Robinson
    Modified by Alex and Clark
'''

# Import libraries
from pygame import *
from Logical_Layer.Viewport.screen_surface import Screen
from Logical_Layer.Viewport.image_scale import ImageScale
from Logical_Layer.Viewport.text_scale import TextScale
from Logical_Layer.Util.color import Color
from Logical_Layer.Util.align import Align
from Logical_Layer.Util.text import Text
from Logical_Layer.Entities.life import Life
from Logical_Layer.Entities.ship import Ship
from Logical_Layer.Entities.enemy import Enemy
from Logical_Layer.Entities.enemies_group import EnemiesGroup
from Logical_Layer.Entities.mistery import Mystery
from Logical_Layer.Entities.blocker import Blocker
from Logical_Layer.Entities.bullet import Bullet
from Logical_Layer.Effects.ship_explosion import ShipExplosion
from Logical_Layer.Effects.enemy_explosion import EnemyExplosion
from Logical_Layer.Effects.mistery_explosion import MysteryExplosion
from Logical_Layer.Players.a3c_observer import A3C_Observer
from Logical_Layer.Players.dqn_observer import DQN_Observer
from Logical_Layer.Players.human_observer import Human_Observer
from random import choice
import sys, os

# Path resources
FULL_PATH = os.getcwd()
FONT_PATH = FULL_PATH + '/Assets/Fonts/'
IMAGE_PATH = FULL_PATH + '/Assets/Images/Doom/'
SOUND_PATH = FULL_PATH + '/Assets/Sounds/Doom/'
FONT = FONT_PATH + 'space_invaders.ttf'

IMG_NAMES = ['ship', 'mystery',
             'enemy1_1', 'enemy1_2',
             'enemy2_1', 'enemy2_2',
             'enemy3_1', 'enemy3_2',
             'explosion_blue', 'explosion_green', 'explosion_purple',
             'laser', 'enemy_laser', 'life']

class SpaceInvaders():
    # Parameterized Constructor
    def __init__(self, scale: int, controlGame: int, gameWindow: Screen, width : float, height: float, leftPos: int = 0, topPos : int = 0):
        # Background sound
        mixer.pre_init(44100, -16, 1, 4096)
        mixer.Sound(SOUND_PATH + 'd_e1m1.wav').play()

        # Select the screen dimension and set with a background image
        self.subWindow = gameWindow.surface.subsurface(Rect(leftPos, topPos, width, height))
        self.screen = Screen(self.subWindow)
        self.background = image.load(IMAGE_PATH + 'background.jpg').convert()
        self.background = ImageScale.scale(self.background, width, height)
        self.scale = scale

        self.images = {name: image.load(IMAGE_PATH + '{}.png'.format(name)).convert_alpha() for name in IMG_NAMES}
        scaleBlock = { 1: 0.77, 2: 0.81, 3: 0.75 } 
    
        # Create scaling objects for images, text, and positions
        self.SHIP = ImageScale(self.scale, self.images['ship'], 70)
        self.LIFE = ImageScale(self.scale, self.images['life'], 40)
        self.ENEMY = ImageScale(self.scale, self.images, 70)
        self.MISTERY = ImageScale(self.scale, self.images, 95)
        self.TextMenu = TextScale(self.scale, 70)

        # Create texts that will be used on the screen
        self.titleText = Text('Doom Invaders', FONT, self.TextMenu.scaleSize, Color.WHITE, self.screen.halfWidth, self.screen.heightP(20), Align.CENTER)      
        self.titleText2 = Text('Press any key to continue', FONT, self.titleText.size - 30, Color.WHITE, self.screen.halfWidth, self.titleText.textHeight, Align.CENTER)     
        self.enemy1Text = Text('   =   10 pts', FONT, self.titleText2.size, Color.GREEN, self.screen.halfWidth, self.titleText2.textHeight + 20)                 
        self.enemy2Text = Text('   =  20 pts', FONT, self.enemy1Text.size, Color.BLUE, self.enemy1Text.xPos , self.enemy1Text.textHeight + 20)                   
        self.enemy3Text = Text('   =  30 pts', FONT, self.enemy2Text.size, Color.PURPLE, self.enemy2Text.xPos , self.enemy2Text.textHeight + 20)                  
        self.enemy4Text = Text('   =  ?????', FONT, self.enemy3Text.size, Color.RED, self.enemy3Text.xPos ,self.enemy3Text.textHeight + 20)                      
        self.gameOverText = Text('Game Over', FONT, self.titleText.size, Color.WHITE, self.screen.widthP(50), self.screen.heightP(35), Align.CENTER)                   
        self.nextRoundText = Text('Next Round', FONT, self.gameOverText.size, Color.WHITE, self.screen.widthP(50), self.screen.heightP(35), Align.CENTER)    

        # Create player lives and group them
        self.life1 = Life(self.screen, self.LIFE, self.screen.width - self.LIFE.scaleSize - 12, 5)
        self.life2 = Life(self.screen, self.LIFE, self.life1.posX - self.LIFE.scaleSize - 8, self.life1.posY)
        self.life3 = Life(self.screen, self.LIFE, self.life2.posX - self.LIFE.scaleSize - 8, self.life2.posY)        
        self.livesGroup = sprite.Group(self.life3, self.life2, self.life1)
        
        self.ScoreTextW = TextScale.scaleWidth('Lives', FONT, self.titleText.size - 30)
        self.scoreText = Text('Score', FONT, self.titleText.size - 30, Color.WHITE, self.screen.widthP(2), 5)
        self.livesText = Text('Lives ', FONT, self.scoreText.size, Color.WHITE, self.life3.posX - self.ScoreTextW - 10, 3)

        scaleEnemyPosition = { 1: self.scoreText.textHeight + (self.MISTERY.scaleSize // 2), 2: 140, 3: 58}
        self.ENEMY_MOVE_DOWN = 35
        self.Enemy_DEFAULT_POSITION = scaleEnemyPosition[scale]
        self.BLOCKER_POSITION = int(self.screen.height * scaleBlock[scale])
        self.groupEnemyPosition = self.Enemy_DEFAULT_POSITION

        # Control of game states and selection of the type of player as well as its mobility
        self.startGame = False
        self.mainScreen = True
        self.gameOver = False
        self.command_left = False
        self.command_right = False
        self.command_shoot = False
        self.observer = self.determineObserver(controlGame)

    # Reset objects and variables to start a new game
    def restartGame(self, score: int):
        self.player = Ship(self.screen, self.SHIP)
        self.playerGroup = sprite.Group(self.player)
        self.explosionsGroup = sprite.Group()
        self.bullets = sprite.Group()
        self.mysteryShip = Mystery(self.screen, self.MISTERY, -100, self.scoreText.textHeight)
        self.mysteryGroup = sprite.Group(self.mysteryShip)
        self.enemyBullets = sprite.Group()
        self.make_enemies()
        self.allSprites = sprite.Group(self.player, self.enemies, self.livesGroup, self.mysteryShip)
        self.keys = key.get_pressed()

        self.timer = time.get_ticks()
        self.noteTimer = time.get_ticks()
        self.shipTimer = time.get_ticks()
        self.score = score
        self.create_audio()
        self.makeNewShip = False
        self.shipAlive = True

    # Run the game
    def main(self):
        if self.mainScreen:
            self.subWindow.blit(self.background, (0, 0))
            self.titleText.draw(self.subWindow)
            self.titleText2.draw(self.subWindow)
            self.enemy1Text.draw(self.subWindow)
            self.enemy2Text.draw(self.subWindow)
            self.enemy3Text.draw(self.subWindow)
            self.enemy4Text.draw(self.subWindow)
            self.create_main_menu()
            for e in event.get():
                if self.should_exit(e):
                    sys.exit()
                if e.type == KEYUP:
                    # Only create blockes on a new game, not a new round
                    self.make_group_blockers(6)
                    self.livesGroup.add(self.life1, self.life2, self.life3)
                    self.restartGame(0)
                    self.startGame = True
                    self.mainScreen = False

        elif self.startGame:
            if not self.enemies and not self.explosionsGroup:
                currentTime = time.get_ticks()
                if currentTime - self.gameTimer < 3000:
                    self.subWindow.blit(self.background, (0, 0))
                    self.scoreNumber = Text(str(self.score), FONT, self.scoreText.size + 2, Color.GREEN, self.scoreText.textWidth + 12, self.scoreText.yPos - 1)
                    self.scoreText.draw(self.subWindow)
                    self.scoreNumber.draw(self.subWindow)
                    self.nextRoundText.draw(self.subWindow)
                    self.livesText.draw(self.subWindow)
                    self.livesGroup.update()
                    self.check_input_player()
                if currentTime - self.gameTimer > 3000:
                    self.groupEnemyPosition += self.ENEMY_MOVE_DOWN    # Move enemies closer to bottom
                    self.restartGame(self.score)
                    self.gameTimer += 3000
            else:
                currentTime = time.get_ticks()
                self.play_main_music(currentTime)
                self.subWindow.blit(self.background, (0, 0))
                self.allBlockers.update(self.subWindow)
                self.scoreNumber = Text(str(self.score), FONT, self.scoreText.size + 2, Color.GREEN, self.scoreText.textWidth + 12, self.scoreText.yPos - 1)
                self.scoreText.draw(self.subWindow)
                self.scoreNumber.draw(self.subWindow)
                self.livesText.draw(self.subWindow)
                self.check_input_player()
                self.enemies.update(currentTime)
                self.allSprites.update(self.keys, currentTime)
                self.explosionsGroup.update(currentTime)
                self.check_collisions()
                self.make_new_ship(self.makeNewShip, currentTime, self.player)
                self.make_enemies_shoot()
                self.observer.update(self.player.rect.x, self.enemies, self.bullets)

        elif self.gameOver:
            currentTime = time.get_ticks()
            self.groupEnemyPosition = self.Enemy_DEFAULT_POSITION             # Reset enemy starting position
            self.create_game_over(currentTime)

    # Temporary menu for the game
    def create_main_menu(self):
        scaleImage = { 1: 60, 2: 50, 3: 40}
        size = scaleImage[self.scale]

        self.enemy1 = self.images['enemy3_1']
        self.enemy1 = transform.scale(self.enemy1, (size, size))
        self.enemy2 = self.images['enemy2_2']
        self.enemy2 = transform.scale(self.enemy2, (size, size))
        self.enemy3 = self.images['enemy1_2']
        self.enemy3 = transform.scale(self.enemy3, (size, size))
        self.enemy4 = self.images['mystery']
        self.enemy4 = transform.scale(self.enemy4, (size + 40, size))

        moveLeft = 70
        moveUp = 10
        self.subWindow.blit(self.enemy1, (self.enemy1Text.xPos - moveLeft, self.enemy1Text.yPos - moveUp))
        self.subWindow.blit(self.enemy2, (self.enemy1Text.xPos - moveLeft, self.enemy2Text.yPos - moveUp))
        self.subWindow.blit(self.enemy3, (self.enemy1Text.xPos - moveLeft, self.enemy3Text.yPos - moveUp))
        self.subWindow.blit(self.enemy4, (self.enemy1Text.xPos - moveLeft - 20, self.enemy4Text.yPos - moveUp + 5))

    # Game over meny
    def create_game_over(self, currentTime):
        self.subWindow.blit(self.background, (0, 0))
        passed = currentTime - self.timer
        if passed < 750:
            self.gameOverText.draw(self.subWindow)
        elif 750 < passed < 1500:
            self.subWindow.blit(self.background, (0, 0))
        elif 1500 < passed < 2250:
            self.gameOverText.draw(self.subWindow)
        elif 2250 < passed < 2750:
            self.subWindow.blit(self.background, (0, 0))
        elif passed > 3000:
            self.mainScreen = True

        for e in event.get():
            if self.should_exit(e):
                sys.exit()

    # Determine the player who will play the game
    def determineObserver(self, type: int):
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

    # Determine the types of ship's movements
    def command(self, command):
        if command == "left":
            self.command_left = True
        elif command == "right":
            self.command_right = True
        elif command == "shoot":
            self.command_shoot = True

    # Check the input handle the ship limits and movement
    def check_input_player(self):
        self.keys = key.get_pressed()
        for e in event.get():
            if self.should_exit(e):
                sys.exit()
        if self.command_left:
            if self.player.rect.x > 10:
                self.player.rect.x -= self.player.speed
            self.command_left = False
        if self.command_right:
            if self.player.rect.x < (self.screen.width - self.SHIP.scaleSize - 10): 
                self.player.rect.x += self.player.speed
            self.command_right = False
        if self.command_shoot:
            if len(self.bullets) == 0 and self.shipAlive:
                if self.score < 5:
                    bullet = Bullet(self.screen, self.player.rect.centerx, self.player.rect.top - 9, -1, 15, self.images['laser'], 'center')
                    self.bullets.add(bullet)
                    self.allSprites.add(self.bullets)
                    self.sounds['shoot2'].play()
                else:
                    leftbullet = Bullet(self.screen, self.player.rect.centerx - 15, self.player.rect.top - 9, -1, 15, self.images['laser'], 'left')
                    rightbullet = Bullet(self.screen, self.player.rect.centerx + 15, self.player.rect.top - 9, -1, 15, self.images['laser'], 'right')
                    self.bullets.add(leftbullet)
                    self.bullets.add(rightbullet)
                    self.allSprites.add(self.bullets)
                    self.sounds['shoot2'].play()
            self.command_shoot = False

    # Create a block made up of individual squares
    def make_blockers(self, number, totalGroups):
        # Number of blocks in rows and columns
        rows = 4
        columns = 9

        # Determine the size of the block based on the scale parameter
        scaleBlocks = [16, 10, 5]
        size = scaleBlocks[self.scale - 1]

        # Determine the position of the first block
        positionBlock = self.screen.width // totalGroups

        # Space between the left wall towards the first block
        if number > 1:
            leftSpace = positionBlock // 4  # This is divided by four to calculate 20% of the initial position of the block
        else:
            halfScreenWidth = positionBlock // 2                # Get half screen
            blockWidth = (columns - 1) * size                   # Get the width of the entire block
            leftSpace =  halfScreenWidth - (blockWidth // 2.5)  # Position the entire block in the middle of the screen

        # Add small piece of a block to form a complete block
        blockerGroup = sprite.Group()
        for row in range(rows):
            for column in range(columns):
                blocker = Blocker(self.screen, size, Color.GREEN, row, column)
                
                # Represents the position on the x-axis
                blocker.rect.x =  leftSpace + (positionBlock * number) + (column * blocker.width) 

                # Represents the position on the y-axis
                blocker.rect.y =  self.BLOCKER_POSITION + (row * blocker.height)

                # Add blocker to the group
                blockerGroup.add(blocker)

        return blockerGroup

    # Create an 'N' number of blocks
    def make_group_blockers(self, numberGroups: int):
        # Limit the number of blockers' group
        if(numberGroups > 6):
            raise Exception("\nThe maximum limit is only 6 blocks. \nAs there are many blocks on the screen, they go outside its limits.")

        # Create block groups and assign them to allBlockers variable
        self.allBlockers = sprite.Group()
        for number in range(numberGroups):
            self.allBlockers.add(self.make_blockers(number, numberGroups))

    # Create a group of enemies
    def make_enemies(self):
        # Extra space between images
        self.extraSpace = { 1: 23, 2: 15, 3: 10 }

        # Number of columns and rows of enemies
        enemyColumns = 10
        enemyRows = 5
        
        # Create group of enemies
        enemies = EnemiesGroup(self.groupEnemyPosition, self.ENEMY_MOVE_DOWN, self.ENEMY.scaleSize, self.screen.width, enemyColumns, enemyRows)
        leftSpace = self.screen.widthP(10)   # A left space of the windows

        for row in range(enemyRows):
            for column in range(enemyColumns):
                enemy = Enemy(self.screen, self.ENEMY, row, column)
                enemy.rect.x = leftSpace + (column * (self.ENEMY.scaleSize + self.extraSpace[self.scale]))  # LeftSpace + Image width + Extra Space
                enemy.rect.y = self.groupEnemyPosition + (row * (self.ENEMY.scaleSize + 8))                 # Enemy position + Image height + Extra Space
                enemies.add(enemy)

        self.enemies = enemies

    # Create enemies' shoots in random order
    def make_enemies_shoot(self):
        if (time.get_ticks() - self.timer) > 700 and self.enemies:
            enemy = self.enemies.random_bottom()
            self.enemyBullets.add(Bullet(self.screen, enemy.rect.centerx, enemy.rect.centery + 10, 1, 5, self.images['enemy_laser'], 'center'))
            self.allSprites.add(self.enemyBullets)
            self.timer = time.get_ticks()

    # Create a new ship when a life is lost
    def make_new_ship(self, createShip: bool, currentTime: int, shipCoor: Ship):
        if createShip and (currentTime - self.shipTimer > 900):
            self.makeNewShip = False
            self.player = Ship(self.screen, self.SHIP, shipCoor.rect.x, shipCoor.rect.y)
            self.allSprites.add(self.player)
            self.playerGroup.add(self.player)
            self.shipAlive = True

    # Calculate game's score
    def calculate_score(self, row):
        scores = {0: 30,
                  1: 20,
                  2: 20,
                  3: 10,
                  4: 10,
                  5: choice([50, 100, 150, 300])
                  }

        score = scores[row]
        self.score += score
        return score

    # Check collisions of the objects
    def check_collisions(self):
        # Detect collision of enemies' bullets and ship's bullets
        sprite.groupcollide(self.bullets, self.enemyBullets, True, True)

        # Detect collision of enemies and ship's bullets
        for enemy in sprite.groupcollide(self.enemies, self.bullets, True, True).keys():
            self.sounds['invaderkilled'].play()
            self.calculate_score(enemy.row)
            EnemyExplosion(self.screen, enemy, self.explosionsGroup)
            self.gameTimer = time.get_ticks()

        # Detect collision of Mystery enemy and ship's bullets
        for mystery in sprite.groupcollide(self.mysteryGroup, self.bullets, True, True).keys():
            mystery.mysteryEntered.stop()
            self.sounds['mysterykilled'].play()
            score = self.calculate_score(mystery.row)
            MysteryExplosion(self.screen, mystery, score, self.explosionsGroup)
            mysteryShip = Mystery(self.screen, self.MISTERY, -100, self.scoreText.textHeight)
            self.allSprites.add(mysteryShip)
            self.mysteryGroup.add(mysteryShip)

        # Detect collision of ship and enemies' bullets
        for player in sprite.groupcollide(self.playerGroup, self.enemyBullets, True, True).keys():
            if self.life1.alive():
                self.life1.kill()
            elif self.life2.alive():
                self.life2.kill()
            elif self.life3.alive():
                self.life3.kill()
            else:
                self.gameOver = True
                self.startGame = False
            self.sounds['shipexplosion'].play()
            ShipExplosion(self.screen, player, self.explosionsGroup)
            self.makeNewShip = True
            self.shipTimer = time.get_ticks()
            self.shipAlive = False

        # Determine the collision of enemies with the ship
        heightBound = self.screen.heightP(90)
        if self.enemies.collisionVertLimit >= heightBound:
            sprite.groupcollide(self.enemies, self.playerGroup, True, True)
            if not self.player.alive() or self.enemies.collisionVertLimit >= self.screen.height:
                self.gameOver = True
                self.startGame = False

        # Determine the collision of the enemies with the blocks
        if self.enemies.collisionVertLimit >= self.BLOCKER_POSITION:
            sprite.groupcollide(self.enemies, self.allBlockers, False, True)

        # Determine the collision of the ship's bullets and the blocks
        sprite.groupcollide(self.bullets, self.allBlockers, True, True)

        # Determine the collision of the enemy's bullets and the blocks
        sprite.groupcollide(self.enemyBullets, self.allBlockers, True, True)  


    def create_audio(self):
        self.sounds = {}
        for sound_name in ['shoot', 'shoot2', 'invaderkilled', 'mysterykilled',
                           'shipexplosion']:
            self.sounds[sound_name] = mixer.Sound(SOUND_PATH + '{}.wav'.format(sound_name))
            self.sounds[sound_name].set_volume(0.2)

        self.musicNotes = [mixer.Sound(SOUND_PATH + '{}.wav'.format(i)) for i
                           in range(4)]
        for sound in self.musicNotes:
            sound.set_volume(0.5)

        self.noteIndex = 0


    def play_main_music(self, currentTime):
        if currentTime - self.noteTimer > self.enemies.moveTime:
            self.note = self.musicNotes[self.noteIndex]
            if self.noteIndex < 3:
                self.noteIndex += 1
            else:
                self.noteIndex = 0

            self.note.play()
            self.noteTimer += self.enemies.moveTime

    @staticmethod
    def should_exit(evt):
        return evt.type == QUIT or (evt.type == KEYUP and evt.key == K_ESCAPE)         # type: (pygame.event.EventType) -> bool
