''' SPACE INVADERS
    Created by Lee Robinson
    Modified by Alex and Clark
'''

# Import libraries
from pygame import *
from Logical_Layer.Viewport.image_scale import ImageScale
from Logical_Layer.Viewport.text_scale import TextScale
from Logical_Layer.Util.color import Color
from Logical_Layer.Util.align import Align
from Logical_Layer.Util.text import Text
from Logical_Layer.Util.limit import Limit
from Logical_Layer.Entities.life import Life
from Logical_Layer.Entities.ship import Ship
from Logical_Layer.Entities.enemy import Enemy
from Logical_Layer.Entities.enemies import EnemiesGroup
from Logical_Layer.Entities.mistery import Mystery
from Logical_Layer.Entities.blocker import Blocker
from Logical_Layer.Entities.bullet import Bullet
from Logical_Layer.Effects.ship_explosion import ShipExplosion
from Logical_Layer.Effects.enemy_explosion import EnemyExplosion
from Logical_Layer.Effects.mistery_explosion import MysteryExplosion
from Logical_Layer.Interfaces.viewport import Viewport
from Logical_Layer.Entities.players import playersGroup
from Logical_Layer.Entities.player import Player

class SpaceInvaders(Viewport):
    gameCount = 0

    # Parameterized Constructor
    def __init__(self, modeGame : int, players : list, difficulty : bool, width : float, height : float, leftPos : int = 0, topPos : int = 0):
        # Initialize super class
        super().__init__("Space Invaders", width, height, leftPos, topPos)    
       
        # Get constructor's attributes
        self.difficulty = difficulty
        self.scale = modeGame

        # Evaluate difficulty changes
        self.numberLives = 3 if self.difficulty else 2
        self.numberBlockers = 6 if self.difficulty else 3
        self.numberEnemiesColumns = 8 if self.difficulty else 10
        self.numberEnemiesRows = 5 if self.difficulty else 6
        self.speedEnemies = 15 if self.difficulty else 20

        # Initialize mixer instance and count game instance
        SpaceInvaders.gameCount += 1
        self.instanceCount = SpaceInvaders.gameCount        
        mixer.pre_init(44100, -16, 1, 4096)
        
        # Names of images
        singularImgs = ['ship1', 'ship2','mystery','enemy1_1', 'enemy1_2', 'enemy2_1', 'enemy2_2','enemy3_1', 'enemy3_2',
                      'explosion_blue', 'explosion_green', 'explosion_purple','laser', 'enemy_laser', 'life', 'background.jpg']

        # Load images and font
        self.images = self.loadSingularImages(singularImgs, self.difficulty)
        self.images =  self.images['basic'] if self.difficulty else self.images['doom']
        self.font = self.getFont()

        # Play background sound
        self.soundPath = self.getSoundPath(self.difficulty)
        if self.instanceCount == 1:
            mixer.Sound(self.soundPath + 'd_e1m1.wav').play(-1)

        # Set a background image
        self.background = transform.scale(self.images['background'], (self.displaySub.width, self.displaySub.height))

        # Create scaling objects for images and text
        self.SHIP1 = ImageScale(self.scale, self.images['ship1'], 70, 70)
        self.SHIP2 = ImageScale(self.scale, self.images['ship2'], 70, 70)
        self.LIFE = ImageScale(self.scale, self.images['life'], 40, 40)
        self.MISTERY = ImageScale(self.scale, self.images['mystery'], 95, 70)
        self.text = TextScale(self.scale, 70)
        shipList = [self.SHIP1, self.SHIP2]

        # Determine ship and text postion
        shipSize = self.SHIP1.scaleWidth
        shipCoord = [self.displaySub.widthP(25) - (shipSize)/2, self.displaySub.widthP(75) - (shipSize)/2] if len(players) == 2 else [0, 0]
        shipText = '{} \t\t & \t\t {}'.format(players[0]['name'], players[1]['name']) if len(players) == 2 else players[0]['name']

        # Create player according to the list of players
        self.playerGroup = playersGroup(self.displaySub, shipList, self.LIFE, self.numberLives, self.displaySub.width - self.LIFE.scaleWidth - 12, 5)

        for index, playerInfo in enumerate(players):
            player = Player(self.displaySub, playerInfo['name'], playerInfo['typePlayer'], self.SHIP1, self.images['laser'], self.playerGroup.scoreLimit, shipCoord[index])
            self.playerGroup.add(player)

        # Create game's HUB
        spriteLife : Life =  self.playerGroup.lives.sprites()[self.numberLives - 1]
        self.ScoreTextW = TextScale.scaleWidth('Lives', self.font, self.text.scaleSize - 30)
        self.scoreText = Text('Score', self.font, self.text.scaleSize - 30, Color.WHITE, self.displaySub.widthP(2), 5)
        self.livesText = Text('Lives ', self.font, self.scoreText.size, Color.WHITE, spriteLife.posX - self.ScoreTextW - 10, 3)
        self.PlayerName = Text(shipText, self.font, self.scoreText.size, Color.WHITE, self.displaySub.widthP(50), 5, Align.CENTER)

        # Create game's extra text
        self.gameOverText = Text('Game Over', self.font, self.text.scaleSize, Color.WHITE, self.displaySub.widthP(50), self.displaySub.heightP(35), Align.CENTER)                   
        self.nextRoundText = Text('Next Round', self.font, self.gameOverText.size, Color.WHITE, self.displaySub.widthP(50), self.displaySub.heightP(35), Align.CENTER)    

        # Determine the initial position of the group of enemies
        self.Enemy_DEFAULT_POSITION = self.scoreText.textHeight + 15
        self.groupEnemyPosition = self.Enemy_DEFAULT_POSITION

        # Control of game states and selection of the type of player as well as its mobility
        self.startGame = False
        self.mainScreen = True
        self.gameOver = False

    def handle_events(self, events) -> dict:
        for event in events:
            if event.type == KEYDOWN:
                match event.key:
                    case _:
                        pass
            else:
                self.exit(event)

    # Run the game
    def draw(self):
        # Initial Game's state
        if self.mainScreen:
            self.screenSub.blit(self.background, (0, 0))
            self.make_group_blockers(self.numberBlockers)
            self.playerGroup.renewLives()
            self.restartGame(0)
            self.startGame = True
            self.mainScreen = False

        # Start Game
        elif self.startGame:
            # Conditional when you win one game (All enemies are dead)
            if not self.enemies and not self.explosionsGroup:
                currentTime = time.get_ticks()
                if currentTime - self.gameTimer < 3000:
                    self.screenSub.blit(self.background, (0, 0))
                    self.scoreNumber = Text(str(self.score), self.font, self.scoreText.size + 2, Color.GREEN1, self.scoreText.textWidth + 12, self.scoreText.yPos - 1)
                    self.scoreText.draw(self.screenSub)
                    self.scoreNumber.draw(self.screenSub)
                    self.nextRoundText.draw(self.screenSub)
                    self.livesText.draw(self.screenSub)
                    self.PlayerName.draw(self.screenSub)
                    self.check_input_player()
                if currentTime - self.gameTimer > 3000:
                    self.restartGame(self.score)
                    self.groupEnemyPosition += self.enemies.verticalVelocity    # Move enemies closer to bottom
                    self.gameTimer += 3000
            
            # Conditional while playing (Updates all game elements)
            else:
                currentTime = time.get_ticks()
                self.play_main_music(currentTime)
                self.screenSub.blit(self.background, (0, 0))
                self.allBlockers.update(self.screenSub)
                self.scoreNumber = Text(str(self.score), self.font, self.scoreText.size + 2, Color.GREEN1, self.scoreText.textWidth + 12, self.scoreText.yPos - 1)
                self.scoreText.draw(self.screenSub)
                self.scoreNumber.draw(self.screenSub)
                self.livesText.draw(self.screenSub)
                self.PlayerName.draw(self.screenSub)
                self.check_input_player()
                self.enemies.update(currentTime)
                self.allSprites.update(self.keys, currentTime)
                self.explosionsGroup.update(currentTime)
                self.check_collisions()
                self.make_new_ship(self.makeNewShip, currentTime)
                self.make_enemies_shoot()

            self.playerGroup.update(self.enemies)

        # End Game
        elif self.gameOver:
            currentTime = time.get_ticks()
            self.groupEnemyPosition = self.Enemy_DEFAULT_POSITION   # Reset enemy starting position
            self.create_game_over(currentTime)

    # Reset objects and variables to start a new game
    def restartGame(self, score: int):
        self.make_enemies()
        self.explosionsGroup = sprite.Group()
        self.bullets = sprite.Group()
        self.mysteryShip = Mystery(self.displaySub, self.MISTERY, self.enemies, -100, self.scoreText.textHeight)
        self.mysteryGroup = sprite.Group(self.mysteryShip)
        self.enemyBullets = sprite.Group()
        self.allSprites = sprite.Group(self.enemies, self.mysteryShip, self.playerGroup.ships)
        self.keys = key.get_pressed()
        self.timer = time.get_ticks()
        self.noteTimer = time.get_ticks()
        self.shipTimer = time.get_ticks()
        self.score = score
        self.create_audio()
        self.makeNewShip = False
        player : Player
        for player in self.playerGroup.sprites():
            player.shipAlive = True

    # Game over meny
    def create_game_over(self, currentTime):
        self.screenSub.blit(self.background, (0, 0))
        passed = currentTime - self.timer
        if passed < 750:
            self.gameOverText.draw(self.screenSub)
        elif 750 < passed < 1500:
            self.screenSub.blit(self.background, (0, 0))
        elif 1500 < passed < 2250:
            self.gameOverText.draw(self.screenSub)
        elif 2250 < passed < 2750:
            self.screenSub.blit(self.background, (0, 0))
        elif passed > 3000:
            self.mainScreen = True

    # Check the input handle the ship limits and movement
    def check_input_player(self):
        # Check input
        player : Player
        for player in self.playerGroup.sprites():
            player.checkInput(self.playerGroup.score, self.sounds)

        # Upgrade ship to two cannons
        self.playerGroup.upgradeShip()

    # Create an 'N' number of blocks
    def make_group_blockers(self, numberGroups: int):
        # Limit the number of blockers' group
        if(numberGroups > 6):
            raise Exception("\nThe maximum limit is only 6 blocks. \nAs there are many blocks on the screen, they go outside its limits.")

        # Create block groups and assign them to allBlockers variable
        self.allBlockers = sprite.Group()
        for number in range(numberGroups):
            self.allBlockers.add(self.make_blockers(number, numberGroups))

    # Create a block made up of individual squares
    def make_blockers(self, number, totalGroups):
        # Number of blocks in rows and columns
        rows = 4
        columns = 9

        # Determine the size of the block based on the scale parameter
        scaleBlocks = [16, 10, 7]
        size = scaleBlocks[self.scale - 1]

        # Determine the position of the blocks on the y-axis
        blockHeight = size * rows
        shipHeight = self.SHIP1.scaleHeight
        spaceShipBlock = 50
        self.blockerPosition = self.displaySub.height - blockHeight - shipHeight - spaceShipBlock

        # Determine the position of the first block on the x-axis
        positionBlock = self.displaySub.width // totalGroups

        # Space between the left wall towards the first block
        if totalGroups > 1:
            leftSpace = positionBlock // 4                             # Space will be a quarter of the position of the first block
        else:
            blockWidth = columns * size                                # Get the width of the entire block
            leftSpace =  self.displaySub.halfWidth  - (blockWidth / 2)     # Position the entire block in the middle of the screen

        # Add small piece of a block to form a complete block
        blockerGroup = sprite.Group()
        for row in range(rows):
            for column in range(columns):
                # Create an individual block
                blocker = Blocker(self.displaySub, size, Color.GREEN1, row, column)
                
                # Draw the individual block in its x-axis position.
                blocker.rect.x =  leftSpace + (positionBlock * number) + (column * blocker.width) 

                # Draw the individual block in its y-axis position.
                blocker.rect.y =  self.blockerPosition + (row * blocker.height)

                # Add blocker to the group
                blockerGroup.add(blocker)

        return blockerGroup

    # Create a group of enemies
    def make_enemies(self):
        # Extra space between images
        self.extraSpace = { 1: 23, 2: 15, 3: 10 }

        # Number of columns and rows of enemies
        enemyColumns = self.numberEnemiesColumns
        enemyRows = self.numberEnemiesRows
        
        # Create group of enemies
        enemySize = ImageScale(self.scale, self.images['enemy1_1'], 68, 63, 0.72)
        enemySpace =  enemySize.scaleHeight + 8                              # Image height + Extra Space
        enemies = EnemiesGroup(self.groupEnemyPosition, enemySpace, self.displaySub, enemyColumns, enemyRows, self.speedEnemies)
        leftSpace = self.displaySub.widthP(10)   # A left space of the windows

        for row in range(enemyRows):
            for column in range(enemyColumns):
                enemy = Enemy(self.displaySub, self.scale, self.images, enemySize, row, column, enemyRows)
                enemy.rect.x = leftSpace + (column * (enemy.scale.scaleWidth + self.extraSpace[self.scale]))   # LeftSpace + Image width + Extra Space
                enemy.rect.y = self.groupEnemyPosition + (row * enemySpace)                                    # Enemy position + Enemy space
                enemies.add(enemy)

        self.enemies = enemies

    # Create enemies' shoots in random order
    def make_enemies_shoot(self):
        i = 1 if self.difficulty else 2
        if (len(self.enemyBullets)) < i and self.enemies:
            enemy = self.enemies.random_bottom()
            self.enemyBullets.add(Bullet(self.displaySub, enemy.rect.centerx, enemy.rect.centery + 10, 1, 5, self.images['enemy_laser']))
            self.allSprites.add(self.enemyBullets)
            self.timer = time.get_ticks()

    # Create a new ship when a life is lost
    def make_new_ship(self, createShip: bool, currentTime: int):
        player : Player
        if createShip and (currentTime - self.shipTimer > 900):
            for player in self.playerGroup.sprites():
                if player.shipAlive == False:
                    player.renewShip(player.ship.rect.x, player.ship.rect.y)
                    self.allSprites.add(player.ship)

            self.makeNewShip = False

    # Calculate game's score
    def calculate_score(self, score : int):
        self.score += score
        return score

    # Check collisions of the objects
    def check_collisions(self):
        # Declare variables' type
        ship : Ship
        player : Player
        enemy : Enemy  
        mystery : Mystery

        # Detect collision of enemies' bullets and ship's bullets
        sprite.groupcollide(self.playerGroup.bullets, self.enemyBullets, True, True)

        # Detect collision of enemies and ship's bullets 
        for enemy in sprite.groupcollide(self.enemies, self.playerGroup.bullets, True, True).keys():
            self.sounds['invaderkilled'].play()
            self.calculate_score(enemy.score)
            self.playerGroup.improveShoots(enemy.score)
            EnemyExplosion(self.displaySub, self.scale, enemy, self.explosionsGroup)
            self.gameTimer = time.get_ticks()

        # Detect collision of Mystery enemy and ship's bullets
        for mystery in sprite.groupcollide(self.mysteryGroup, self.playerGroup.bullets, True, True).keys():
            mystery.mysteryEntered.stop()
            self.sounds['mysterykilled'].play()
            score = self.calculate_score(mystery.score)
            self.playerGroup.improveShoots(score)
            MysteryExplosion(self.displaySub, mystery, score, self.explosionsGroup)
            mysteryShip = Mystery(self.displaySub, self.MISTERY, self.enemies, -100, self.scoreText.textHeight)
            self.allSprites.add(mysteryShip)
            self.mysteryGroup.add(mysteryShip)

        # Detect collision of ship and enemies' bullets
        for player in self.playerGroup.sprites():
            for ship in sprite.groupcollide(sprite.Group(player.ship), self.enemyBullets, True, True).keys():
                # Remove one life and know remaining lives
                remainingLife = self.playerGroup.removeLife()

                # Finish the game if player does not have lives 
                if remainingLife == 0:
                    self.gameOver = True
                    self.startGame = False

                # Show explosion effect
                self.sounds['shipexplosion'].play()
                ShipExplosion(self.displaySub, ship, self.explosionsGroup)
                
                # Request a new ship
                self.shipTimer = time.get_ticks()
                self.makeNewShip = True
                player.shipAlive = False

        # Determine the collision of enemies with the ship
        heightBound = self.displaySub.heightP(90)
        Limit.horizontalBorder(self.displaySub, Color.WHITE, heightBound)
        if self.enemies.collisionLimit >= heightBound:
            for ship in sprite.groupcollide(self.playerGroup.ships, self.enemies, True, True).keys():
                if not ship.alive() or self.enemies.collisionLimit >= self.displaySub.height:
                    self.gameOver = True
                    self.startGame = False

        # Determine the collision of the enemies with the blocks
        if self.enemies.collisionLimit >= self.blockerPosition:
            sprite.groupcollide(self.enemies, self.allBlockers, False, True)

        # Determine the collision of the ship's bullets and the blocks
        sprite.groupcollide(self.playerGroup.bullets, self.allBlockers, True, True)

        # Determine the collision of the enemy's bullets and the blocks
        sprite.groupcollide(self.enemyBullets, self.allBlockers, True, True)  

    # Create audio
    def create_audio(self):
        self.sounds = {}
        for sound_name in ['shoot1', 'shoot2', 'invaderkilled', 'mysterykilled','shipexplosion']:
            self.sounds[sound_name] = mixer.Sound(self.soundPath + '{}.wav'.format(sound_name))
            self.sounds[sound_name].set_volume(0.2)

        self.musicNotes = [mixer.Sound(self.soundPath + '{}.wav'.format(i)) for i in range(4)]
        for sound in self.musicNotes:
            sound.set_volume(0.5)

        self.noteIndex = 0

    # Play audio
    def play_main_music(self, currentTime):
        if currentTime - self.noteTimer > self.enemies.moveTime:
            self.note = self.musicNotes[self.noteIndex]
            if self.noteIndex < 3:
                self.noteIndex += 1
            else:
                self.noteIndex = 0

            self.note.play()
            self.noteTimer += self.enemies.moveTime