'''
    SPACE INVADERS
    Created by Lee Robinson
    Modified by Alex and Clarck
'''

# Import libraries
import sys, os
from Models import observer
from pygame import *
from random import choice
from enum import Enum

# Path resources
FULL_PATH = os.getcwd()
FONT_PATH = FULL_PATH + '/Resources/Fonts/'
IMAGE_PATH = FULL_PATH + '/Resources/Images/Doom/'
SOUND_PATH = FULL_PATH + '/Resources/Sounds/Doom/'

# Color Variables (R, G, B)
WHITE = (255, 255, 255)
GREEN = (78, 255, 87)
YELLOW = (241, 255, 0)
BLUE = (80, 255, 239)
PURPLE = (203, 0, 255)
RED = (237, 28, 36)
TEAL = (0, 128, 128)
ORANGE = (255, 165, 0)
OLIVE = (128, 128, 0)

COLLISION_REC = False
FONT = FONT_PATH + 'space_invaders.ttf'
IMG_NAMES = ['ship', 'mystery',
             'enemy1_1', 'enemy1_2',
             'enemy2_1', 'enemy2_2',
             'enemy3_1', 'enemy3_2',
             'explosion_blue', 'explosion_green', 'explosion_purple',
             'laser', 'enemy_laser', 'life']

class Collision():
    @classmethod
    def detectionBorders(self, rect: Rect, screen: Surface, color: tuple):
        if COLLISION_REC:
            border = rect.inflate(4, 4)            # Increase by 4 pixels on all sides for a border effect
            draw.rect(screen, color, border)       # Draw the edge of the rectangle

class Ship(sprite.Sprite):
    # Parameterized Constructor
    def __init__(self, gameScreen: Surface, size: int, image: dict):
        sprite.Sprite.__init__(self)
        self.scaleShip = { 1: 70, 2: 55, 3: 40 }                    # Image sizes according to the scale parameter
        self.image = image
        self.image = transform.scale(self.image, (size, size))      # Scale image based on scale parameter
        self.screen = gameScreen                                    # Screen where the content will be drawn
        self.size = size                                            # Size of the image

        self.xPos = self.screen.get_width() // 2                           # Middle position on the screen
        self.yPos = self.screen.get_height() - (size + 4)                  # Height position minus image size
        self.rect = self.image.get_rect(topleft=(self.xPos, self.yPos))
        self.speed = 5

    # Overrides the Update method which is responsible for displaying elements on the screen
    def update(self, keys, *args):
        Collision.detectionBorders(self.rect, self.screen, YELLOW)
        self.screen.blit(self.image, self.rect)


class Bullet(sprite.Sprite):
    # Parameterized Constructor
    def __init__(self, gameScreen: Surface, xPos: int, yPos: int, direction: int, speed: float, image: dict, side: str):
        sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect(topleft=(xPos, yPos))
        self.screen = gameScreen
        self.direction = direction
        self.speed = speed
        self.side = side
   
    # Overrides the Update method which is responsible for displaying elements on the screen
    def update(self, keys, *args):
        Collision.detectionBorders(self.rect, self.screen, BLUE)
        self.screen.blit(self.image, self.rect)
        self.rect.y += self.speed * self.direction
        if self.rect.y < 32 or self.rect.y > self.screen.get_height():
            self.kill()


class Enemy(sprite.Sprite):
    # Parameterized Constructor
    def __init__(self, gameScreen: Surface, size: int, listImages: dict, row: int, column: int):
        sprite.Sprite.__init__(self)
        self.size = size
        self.row = row
        self.column = column
        self.listImages = listImages
        self.images = []
        self.load_images()
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.screen = gameScreen  # Screen where the content will be drawn

    # It creates an animation effect by cycling through a sequence of images
    def toggle_image(self):
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]

    # Overrides the Update method which is responsible for displaying elements on the screen
    def update(self, *args):
        Collision.detectionBorders(self.rect, self.screen, PURPLE)
        self.screen.blit(self.image, self.rect)

    def load_images(self):
        numberEnemy = {0: ['1_2', '1_1'],
                       1: ['2_2', '2_1'],
                       2: ['2_2', '2_1'],
                       3: ['3_1', '3_2'],
                       4: ['3_1', '3_2'],
                      }
        img1, img2 = (self.listImages['enemy{}'.format(img_num)] for img_num in
                      numberEnemy[self.row])
        self.images.append(transform.scale(img1, (self.size, self.size - 5)))
        self.images.append(transform.scale(img2, (self.size, self.size - 5)))


class EnemiesGroup(sprite.Group):
    # Parameterized Constructor
    def __init__(self, enemyPosition: int, enemyMove: int, enemySize: int , width: Surface, columns: int, rows: int):
        sprite.Group.__init__(self)
        self.enemies = [[None] * columns for _ in range(rows)]
        self.columns = columns
        self.rows = rows
        self.leftAddMove = 0
        self.rightAddMove = 0
        self.moveTime = 600
        self.direction = 1
        self.rightMoves = 30
        self.leftMoves = 30
        self.moveNumber = 15
        self.timer = time.get_ticks()
        self.collisionBottom = enemyPosition + ((rows - 1) * (enemySize + 8)) + 35
        self._aliveColumns = list(range(columns))
        self._leftAliveColumn = 0
        self._rightAliveColumn = columns - 1
        self.enemyMove = enemyMove
        self.width = width
   
    # Overrides the Update method which is responsible for displaying elements on the screen
    def update(self, current_time):
        # Conditional that is true when the time is greather than moveTime (600) milliseconds. 
        # This conditional allows to refresh the enemy sprites to create a animation movement effect.
        if current_time - self.timer > self.moveTime:
            if self.direction == 1:
                max_move = self.rightMoves
            else:
                max_move = self.leftMoves

            # The conditional is true the row of enemies moves down
            if self.moveNumber >= max_move:
                self.direction *= -1
                self.moveNumber = 0

                # Toggle all sprites and move them down
                for enemy in self:
                    enemy.rect.y += self.enemyMove
                    enemy.toggle_image()

                # Determine the lower collision point
                numberSprites = len(self)
                if numberSprites > 0:
                    lastRowEnemy = self.sprites()[numberSprites - 1]
                    self.collisionBottom = lastRowEnemy.rect.bottom + self.enemyMove

            else:
                velocity = 10 if self.direction == 1 else -10
                for enemy in self:
                    enemy.rect.x += velocity
                    enemy.toggle_image()
                self.moveNumber += 1

            self.timer += self.moveTime

    def add_internal(self, *sprites):
        super(EnemiesGroup, self).add_internal(*sprites)
        for s in sprites:
            self.enemies[s.row][s.column] = s

    def remove_internal(self, *sprites):
        super(EnemiesGroup, self).remove_internal(*sprites)
        for s in sprites:
            self.kill(s)
        self.update_speed()

    def is_column_dead(self, column):
        return not any(self.enemies[row][column]
                       for row in range(self.rows))

    def random_bottom(self):
        col = choice(self._aliveColumns)
        col_enemies = (self.enemies[row - 1][col]
                       for row in range(self.rows, 0, -1))
        return next((en for en in col_enemies if en is not None), None)

    def update_speed(self):
        if len(self) == 1:
            self.moveTime = 200
        elif len(self) <= 10:
            self.moveTime = 400

    def kill(self, enemy):
        self.enemies[enemy.row][enemy.column] = None
        is_column_dead = self.is_column_dead(enemy.column)
        if is_column_dead:
            self._aliveColumns.remove(enemy.column)

        if enemy.column == self._rightAliveColumn:
            while self._rightAliveColumn > 0 and is_column_dead:
                self._rightAliveColumn -= 1
                self.rightAddMove += 5
                is_column_dead = self.is_column_dead(self._rightAliveColumn)

        elif enemy.column == self._leftAliveColumn:
            while self._leftAliveColumn < self.columns and is_column_dead:
                self._leftAliveColumn += 1
                self.leftAddMove += 5
                is_column_dead = self.is_column_dead(self._leftAliveColumn)


class Blocker(sprite.Sprite):
    # Parameterized Constructor
    def __init__(self, gameScreen: Surface, size: int, color: tuple, row: int, column: int):
        sprite.Sprite.__init__(self)
        self.height = size
        self.width = size
        self.color = color
        self.image = Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.row = row
        self.column = column
        self.screen = gameScreen

    # Overrides the Update method which is responsible for displaying elements on the screen
    def update(self, keys, *args):
        Collision.detectionBorders(self.rect, self.screen, WHITE)
        self.screen.blit(self.image, self.rect)


class Mystery(sprite.Sprite):
    # Parameterized Constructor
    def __init__(self, gameScreen: Surface, scale: int, image: dict):
        sprite.Sprite.__init__(self)
        scaleMisterySize = {1: 95, 2: 90, 3: 78}
        self.image = image
        self.image = transform.scale(self.image, (scaleMisterySize[scale], scaleMisterySize[scale] - 35))
        self.rect = self.image.get_rect(topleft=(-80, 45))
        self.row = 5
        self.moveTime = 25000
        self.direction = 1
        self.timer = time.get_ticks()
        self.mysteryEntered = mixer.Sound(SOUND_PATH + 'mysteryentered.wav')
        self.mysteryEntered.set_volume(0.3)
        self.playSound = True
        self.screen = gameScreen

    # Overrides the Update method which is responsible for displaying elements on the screen
    def update(self, keys, currentTime, *args):
        Collision.detectionBorders(self.rect, self.screen, TEAL)
        resetTimer = False
        passed = currentTime - self.timer
        if passed > self.moveTime:
            if (self.rect.x < 0 or self.rect.x > self.screen.get_width()) and self.playSound:
                self.mysteryEntered.play()
                self.playSound = False
            if self.rect.x < (self.screen.get_width() + 40) and self.direction == 1:
                self.mysteryEntered.fadeout(4000)
                self.rect.x += 2
                self.screen.blit(self.image, self.rect)
            if self.rect.x > -100 and self.direction == -1:
                self.mysteryEntered.fadeout(4000)
                self.rect.x -= 2
                self.screen.blit(self.image, self.rect)
       
        if self.rect.x > self.screen.get_width() + 30:
            self.playSound = True
            self.direction = -1
            resetTimer = True
        if self.rect.x < -90:
            self.playSound = True
            self.direction = 1
            resetTimer = True
        if passed > self.moveTime and resetTimer:
            self.timer = currentTime


class EnemyExplosion(sprite.Sprite):
    # Parameterized Constructor
    def __init__(self, gameScreen: Surface, enemy: Surface, size: int, listImages: dict, *groups):
        super(EnemyExplosion, self).__init__(*groups)
        self.listImages = listImages
        self.image = transform.scale(self.get_image(enemy.row), (size, size))
        self.image2 = transform.scale(self.get_image(enemy.row), (size, size))
        self.rect = self.image.get_rect(topleft=(enemy.rect.x, enemy.rect.y))
        self.timer = time.get_ticks()
        self.screen = gameScreen

    def get_image(self, row):
        img_colors = ['purple', 'blue', 'blue', 'green', 'green']
        return self.listImages['explosion_{}'.format(img_colors[row])]

    # Overrides the Update method which is responsible for displaying elements on the screen
    def update(self, current_time, *args):
        passed = current_time - self.timer
        if passed <= 100:
            self.screen.blit(self.image, self.rect)
        elif passed <= 200:
            self.screen.blit(self.image2, (self.rect.x - 6, self.rect.y - 6))
        elif 400 < passed:
            self.kill()


class MysteryExplosion(sprite.Sprite):
    # Parameterized Constructor
    def __init__(self, gameScreen: Surface, mystery, score: int, *groups):
        super(MysteryExplosion, self).__init__(*groups)
        self.text = Text(str(score), FONT, 20, WHITE, mystery.rect.x + 20, mystery.rect.y + 6)
        self.timer = time.get_ticks()
        self.screen = gameScreen

    # Overrides the Update method which is responsible for displaying elements on the screen
    def update(self, current_time, *args):
        passed = current_time - self.timer
        if passed <= 200 or 400 < passed <= 600:
            self.text.draw(self.screen)
        elif 600 < passed:
            self.kill()


class ShipExplosion(sprite.Sprite):
    # Parameterized Constructor
    def __init__(self, gameScreen: Surface, ship : Ship, *groups):
        super(ShipExplosion, self).__init__(*groups)
        self.image = ship.image
        self.image = transform.scale(self.image, (ship.size, ship.size)) 
        self.rect = self.image.get_rect(topleft=(ship.rect.x, ship.rect.y))
        self.timer = time.get_ticks()
        self.screen = gameScreen

    def update(self, current_time, *args):
        passed = current_time - self.timer
        if 300 < passed <= 600:
            self.screen.blit(self.image, self.rect)
        elif 900 < passed:
            self.kill()


class Life(sprite.Sprite):
    # Parameterized Constructor
    def __init__(self, gameScreen: Surface, xPos: int, yPos: int, scale: int, image: dict):
        sprite.Sprite.__init__(self)
        scaleImage = { 1: 40, 2: 30, 3: 25 } 
        self.image = image
        self.image = transform.scale(self.image, (scaleImage[scale], scaleImage[scale]))
        self.rect = self.image.get_rect(topleft=(xPos, yPos))
        self.screen = gameScreen
        self.imagePosX = self.image.get_width() + xPos
        self.imagePosY = self.image.get_height() + yPos


    def update(self, *args):
        Collision.detectionBorders(self.rect, self.screen, ORANGE)
        self.screen.blit(self.image, self.rect)


class Align(Enum):
    LEFT = 1
    CENTER = 2
    RIGHT = 3

    @classmethod
    def horizontalAlignment(cls, align: Enum, xPos: float, textWidth: float):
        match align:
            case Align.RIGHT:
                return xPos
            case Align.CENTER:
                return xPos - (textWidth // 2)
            case Align.LEFT:
                return xPos - textWidth
            case _:
                return xPos


class Text(object):
    # Parameterized Constructor
    def __init__(self, message: str, textFont: str, letterSize: int, color: tuple, xPos: float , yPos: float, percentageScreen: Surface = None, align: Align = Align.RIGHT):
        self.font = font.Font(textFont, letterSize)
        self.surface = self.font.render(message, True, color)
        self.size = letterSize
        
        # Specify a percentage location which represents a portion of the total screen width and height. 
        if percentageScreen != None:
            if (xPos >= 0 and xPos <= 100) and (yPos >= 0 and yPos <= 100): 
                xPos = (percentageScreen.get_width() * xPos) / 100
                yPos = (percentageScreen.get_height() * yPos) / 100
            else:
                raise Exception("The xPos and yPos must be values between 0 to 100.")

        # Align horizontally based on the given x-axis position 
        xPos = Align.horizontalAlignment(align, xPos, self.surface.get_width())
        self.rect = self.surface.get_rect(topleft=(xPos, yPos))

        # Vertical and horizontal position of the text
        self.xPos, self.yPos = xPos, yPos

        # Position of the text which includes the position in pixels plus the width or height in pixels.
        self.textWidth = self.surface.get_width() +  self.xPos
        self.textHeight = self.surface.get_height() + self.yPos
        self.screen = percentageScreen

    def draw(self, surface):
        if self.screen != None:
            Collision.detectionBorders(self.rect, self.screen, OLIVE)

        surface.blit(self.surface, self.rect)


class SpaceInvaders():
    # Parameterized Constructor
    def __init__(self, scale: int, screen: Surface, width : float, height: float, leftPos: int = 0, topPos : int = 0):
        mixer.pre_init(44100, -16, 1, 4096)
        mixer.Sound(SOUND_PATH + 'd_e1m1.wav').play()

        self.images = {name: image.load(IMAGE_PATH + '{}.png'.format(name)).convert_alpha() for name in IMG_NAMES}

        self.screen = screen.subsurface(Rect(leftPos, topPos, width, height))
        self.background = image.load(IMAGE_PATH + 'background.jpg').convert()
        self.background = transform.scale(self.background, (width, height))
        self.screenWidth = width
        self.screenHeight = height
        self.scale = scale

        self.startGame = False
        self.mainScreen = True
        self.gameOver = False

        scaleBlock = { 1: 0.77, 2: 0.81, 3: 0.75 } 
        scaleText = { 1: 70, 2: 60, 3: 50}
        scaleEnemyPosition = { 1: 70, 2: 140, 3: 58}
        scaleEnemySize = {1: 65, 2: 50, 3: 40}
        scaleShip = { 1: 70, 2: 55, 3: 40 }

        self.ENEMY_MOVE_DOWN = 35
        self.Enemy_DEFAULT_POSITION = scaleEnemyPosition[scale]
        self.BLOCKER_POSITION = int(self.screenHeight * scaleBlock[scale])
        self.groupEnemyPosition = self.Enemy_DEFAULT_POSITION
        self.ENEMY_SIZE = scaleEnemySize[scale]
        self.SHIP_SIZE = scaleShip[scale]

        self.titleText = Text('Doom Invaders', FONT, scaleText[scale], WHITE, 50, 20, self.screen, Align.CENTER)      
        self.titleText2 = Text('Press any key to continue', FONT, self.titleText.size - 30, WHITE, width // 2, self.titleText.textHeight, align=Align.CENTER)     
        self.enemy1Text = Text('   =   10 pts', FONT, self.titleText2.size, GREEN, width // 2, self.titleText2.textHeight + 20)                 
        self.enemy2Text = Text('   =  20 pts', FONT, self.enemy1Text.size, BLUE, self.enemy1Text.xPos , self.enemy1Text.textHeight + 20)                   
        self.enemy3Text = Text('   =  30 pts', FONT, self.enemy2Text.size, PURPLE, self.enemy2Text.xPos , self.enemy2Text.textHeight + 20)                  
        self.enemy4Text = Text('   =  ?????', FONT, self.enemy3Text.size, RED, self.enemy3Text.xPos ,self.enemy3Text.textHeight + 20)                      
        self.scoreText = Text('Score', FONT, self.titleText.size - 30, WHITE, width * 0.02, 5)
        self.livesText = Text('Lives ', FONT, self.scoreText.size, WHITE, 80, 0.5, self.screen)
        self.gameOverText = Text('Game Over', FONT, self.livesText.size, WHITE, 50, 35, self.screen, Align.CENTER)                   
        self.nextRoundText = Text('Next Round', FONT, self.gameOverText.size, WHITE, 50, 35, self.screen, Align.CENTER)    

        self.life1 = Life(self.screen, self.livesText.textWidth + 5, 3, scale, self.images['life'])
        self.life2 = Life(self.screen, self.life1.imagePosX + 5, 3, scale, self.images['life'])
        self.life3 = Life(self.screen, self.life2.imagePosX + 5, 3, scale, self.images['life'])
        self.livesGroup = sprite.Group(self.life1, self.life2, self.life3)
        self.observer = observer.human_observer(self, 0)
        self.command_left = False
        self.command_right = False
        self.command_shoot = False

    def command(self, command):
        if command == "left":
            self.command_left = True
        elif command == "right":
            self.command_right = True
        elif command == "shoot":
            self.command_shoot = True

    def reset(self, score):
        self.player = Ship(self.screen, self.SHIP_SIZE, self.images['ship'])
        self.playerGroup = sprite.Group(self.player)
        self.explosionsGroup = sprite.Group()
        self.bullets = sprite.Group()
        self.mysteryShip = Mystery(self.screen, self.scale, self.images['mystery'])
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

    def make_blockers(self, number, totalBlocks):
        # Limit the number of blocks
        if(totalBlocks > 6):
            raise Exception("\nThe maximum limit is only 6 blocks. \nAs there are many blocks on the screen, they go outside its limits.")

        # Number of blocks in rows and columns
        rows = 4
        columns = 9

        # Determine the size of the block based on the scale parameter
        scaleBlocks = [16, 10, 5]
        size = scaleBlocks[self.scale - 1]

        # Determine the position of the first block
        positionBlock = self.screenWidth // totalBlocks

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
                blocker = Blocker(self.screen, size, GREEN, row, column)
                
                # Represents the position on the x-axis
                blocker.rect.x =  leftSpace + (positionBlock * number) + (column * blocker.width) 

                # Represents the position on the y-axis
                blocker.rect.y =  self.BLOCKER_POSITION + (row * blocker.height)

                # Add blocker to the group
                blockerGroup.add(blocker)

        return blockerGroup

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

    def check_input(self):
        self.keys = key.get_pressed()
        for e in event.get():
            if self.should_exit(e):
                sys.exit()
        if self.command_left:
            if self.player.rect.x > 10:
                self.player.rect.x -= self.player.speed
            self.command_left = False
        if self.command_right:
            if self.player.rect.x < (self.screenWidth * 0.946): #TO_DO : MAY BE CHANGE
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

    def make_enemies(self):
        # Extra space between images
        self.extraSpace = { 1: 23, 2: 15, 3: 10 }

        # Number of columns and rows of enemies
        enemyColumns = 10
        enemyRows = 5
        
        # Create group of enemies
        enemies = EnemiesGroup(self.groupEnemyPosition, self.ENEMY_MOVE_DOWN, self.ENEMY_SIZE, self.screenWidth, enemyColumns, enemyRows)
        leftSpace = self.screenWidth * 0.15  # A percentage space from left based on screen width 

        for row in range(enemyRows):
            for column in range(enemyColumns):
                enemy = Enemy(self.screen, self.ENEMY_SIZE, self.images, row, column)
                enemy.rect.x = leftSpace + (column * (self.ENEMY_SIZE + self.extraSpace[self.scale]))  # LeftSpace + Image width + Extra Space
                enemy.rect.y = self.groupEnemyPosition + (row * (self.ENEMY_SIZE + 8))                # Enemy position + Image height + Extra Space
                enemies.add(enemy)

        self.enemies = enemies

    def make_enemies_shoot(self):
        if (time.get_ticks() - self.timer) > 700 and self.enemies:
            enemy = self.enemies.random_bottom()
            self.enemyBullets.add(Bullet(self.screen, enemy.rect.centerx, enemy.rect.centery + 10, 1, 5, self.images['enemy_laser'], 'center'))
            self.allSprites.add(self.enemyBullets)
            self.timer = time.get_ticks()

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
        self.screen.blit(self.enemy1, (self.enemy1Text.xPos - moveLeft, self.enemy1Text.yPos - moveUp))
        self.screen.blit(self.enemy2, (self.enemy1Text.xPos - moveLeft, self.enemy2Text.yPos - moveUp))
        self.screen.blit(self.enemy3, (self.enemy1Text.xPos - moveLeft, self.enemy3Text.yPos - moveUp))
        self.screen.blit(self.enemy4, (self.enemy1Text.xPos - moveLeft - 20, self.enemy4Text.yPos - moveUp + 5))

    def check_collisions(self):
        # Detect collision of enemies' bullets and ship's bullets
        sprite.groupcollide(self.bullets, self.enemyBullets, True, True)

        # Detect collision of enemies and ship's bullets
        for enemy in sprite.groupcollide(self.enemies, self.bullets, True, True).keys():
            self.sounds['invaderkilled'].play()
            self.calculate_score(enemy.row)
            EnemyExplosion(self.screen, enemy, self.ENEMY_SIZE, self.images, self.explosionsGroup)
            self.gameTimer = time.get_ticks()

        # Detect collision of Mystery enemy and ship's bullets
        for mystery in sprite.groupcollide(self.mysteryGroup, self.bullets, True, True).keys():
            mystery.mysteryEntered.stop()
            self.sounds['mysterykilled'].play()
            score = self.calculate_score(mystery.row)
            MysteryExplosion(self.screen, mystery, score, self.explosionsGroup)
            newShip = Mystery(self.screen, self.scale, self.images['mystery'])
            self.allSprites.add(newShip)
            self.mysteryGroup.add(newShip)

        # Detect collision of ship and enemies' bullets
        for player in sprite.groupcollide(self.playerGroup, self.enemyBullets, True, True).keys():
            if self.life3.alive():
                self.life3.kill()
            elif self.life2.alive():
                self.life2.kill()
            elif self.life1.alive():
                self.life1.kill()
            else:
                self.gameOver = True
                self.startGame = False
            self.sounds['shipexplosion'].play()
            ShipExplosion(self.screen, player, self.explosionsGroup)
            self.makeNewShip = True
            self.shipTimer = time.get_ticks()
            self.shipAlive = False

        # Determine the collision of enemies with the ship
        heightBound = self.screenHeight * 0.90
        if self.enemies.collisionBottom >= heightBound:
            sprite.groupcollide(self.enemies, self.playerGroup, True, True)
            if not self.player.alive() or self.enemies.collisionBottom >= self.screenHeight:
                self.gameOver = True
                self.startGame = False

        # Determine the collision of the enemies with the blocks
        if self.enemies.collisionBottom >= self.BLOCKER_POSITION:
            sprite.groupcollide(self.enemies, self.allBlockers, False, True)

        # Determine the collision of the ship's bullets and the blocks
        sprite.groupcollide(self.bullets, self.allBlockers, True, True)

        # Determine the collision of the enemy's bullets and the blocks
        sprite.groupcollide(self.enemyBullets, self.allBlockers, True, True)

    def create_new_ship(self, createShip, currentTime):
        if createShip and (currentTime - self.shipTimer > 900):
            self.player = Ship(self.screen, self.SHIP_SIZE, self.images['ship'])
            self.allSprites.add(self.player)
            self.playerGroup.add(self.player)
            self.makeNewShip = False
            self.shipAlive = True

    def create_game_over(self, currentTime):
        self.screen.blit(self.background, (0, 0))
        passed = currentTime - self.timer
        if passed < 750:
            self.gameOverText.draw(self.screen)
        elif 750 < passed < 1500:
            self.screen.blit(self.background, (0, 0))
        elif 1500 < passed < 2250:
            self.gameOverText.draw(self.screen)
        elif 2250 < passed < 2750:
            self.screen.blit(self.background, (0, 0))
        elif passed > 3000:
            self.mainScreen = True

        for e in event.get():
            if self.should_exit(e):
                sys.exit()

    def main(self):
        if self.mainScreen:
            self.screen.blit(self.background, (0, 0))
            self.titleText.draw(self.screen)
            self.titleText2.draw(self.screen)
            self.enemy1Text.draw(self.screen)
            self.enemy2Text.draw(self.screen)
            self.enemy3Text.draw(self.screen)
            self.enemy4Text.draw(self.screen)
            self.create_main_menu()
            for e in event.get():
                if self.should_exit(e):
                    sys.exit()
                if e.type == KEYUP:
                    # Only create blockes on a new game, not a new round
                    numberBlocks = 6
                    self.allBlockers = sprite.Group()
                    for number in range(numberBlocks):
                        self.allBlockers.add(self.make_blockers(number, numberBlocks))

                    self.livesGroup.add(self.life1, self.life2, self.life3)
                    self.reset(0)
                    self.startGame = True
                    self.mainScreen = False

        elif self.startGame:
            if not self.enemies and not self.explosionsGroup:
                currentTime = time.get_ticks()
                if currentTime - self.gameTimer < 3000:
                    self.screen.blit(self.background, (0, 0))
                    self.scoreText2 = Text(str(self.score), FONT, self.scoreText.size + 2, GREEN, self.scoreText.textWidth + 12, self.scoreText.yPos - 1)
                    self.scoreText.draw(self.screen)
                    self.scoreText2.draw(self.screen)
                    self.nextRoundText.draw(self.screen)
                    self.livesText.draw(self.screen)
                    self.livesGroup.update()
                    self.check_input()
                if currentTime - self.gameTimer > 3000:
                    self.groupEnemyPosition += self.ENEMY_MOVE_DOWN    # Move enemies closer to bottom
                    self.reset(self.score)
                    self.gameTimer += 3000
            else:
                currentTime = time.get_ticks()
                self.play_main_music(currentTime)
                self.screen.blit(self.background, (0, 0))
                self.allBlockers.update(self.screen)
                self.scoreText2 = Text(str(self.score), FONT, self.scoreText.size + 2, GREEN, self.scoreText.textWidth + 12, self.scoreText.yPos - 1)
                self.scoreText.draw(self.screen)
                self.scoreText2.draw(self.screen)
                self.livesText.draw(self.screen)
                self.check_input()
                self.enemies.update(currentTime)
                self.allSprites.update(self.keys, currentTime)
                self.explosionsGroup.update(currentTime)
                self.check_collisions()
                self.create_new_ship(self.makeNewShip, currentTime)
                self.make_enemies_shoot()
                self.observer.update(self.player.rect.x, self.enemies, self.bullets)

        elif self.gameOver:
            currentTime = time.get_ticks()
            self.groupEnemyPosition = self.Enemy_DEFAULT_POSITION             # Reset enemy starting position
            self.create_game_over(currentTime)


# if __name__ == '__main__':
#     # Variables to control the game
#     optionMenu = 1
#     gameControl = True

#     # Start the video game
#     init()
#     clock = time.Clock()
#     display.set_caption('Space Invaders')
#     screenWidth = display.Info().current_w
#     screenHeight = display.Info().current_h

#     # Set main screen dimensions
#     screen = display.set_mode((screenWidth , screenHeight)) # 800 600

#     IMAGES = {name: image.load(IMAGE_PATH + '{}.png'.format(name)).convert_alpha() for name in IMG_NAMES}

#     # Determine half screen width and height
#     halfScreenWidth = screenWidth / 2
#     halfScreenHeight = screenHeight / 2
    
#     print('Display Mode:')
#     print('{} - {}'.format(screenWidth, screenHeight))

#     # Initialize games depending on the type of game (single player or multiplayer)
#     match optionMenu:
#         case 1:
#             fullScreen = SpaceInvaders(optionMenu, screen, screenWidth, screenHeight)
#         case 2:
#             leftScreen = SpaceInvaders(optionMenu, screen, halfScreenWidth, screenHeight)
#             rightScreen = SpaceInvaders(optionMenu, screen, halfScreenWidth, screenHeight, halfScreenWidth)
#         case 3:
#             leftTop = SpaceInvaders(optionMenu, screen, halfScreenWidth, halfScreenHeight)
#             leftBottom = SpaceInvaders(optionMenu, screen, halfScreenWidth, halfScreenHeight, 0, halfScreenHeight)
#             rightTop = SpaceInvaders(optionMenu, screen, halfScreenWidth, halfScreenHeight, halfScreenWidth)
#             rightBottom = SpaceInvaders(optionMenu, screen, halfScreenWidth, halfScreenHeight, halfScreenWidth, halfScreenHeight)
#         case _:
#             gameControl = False
#             print("Incorrect Menu Option")

#     # Render games 
#     while gameControl:
#         match optionMenu:
#             case 1:
#                 fullScreen.main()
#             case 2:
#                 leftScreen.main()
#                 rightScreen.main()
#             case 3:
#                 leftTop.main()
#                 leftBottom.main()
#                 rightTop.main()
#                 rightBottom.main()
#             case _:
#                 gameControl = False

#         display.update()
#         clock.tick(60)

