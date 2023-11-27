from pygame import *
from Logical_Layer.Viewport.image_scale import ImageScale
from Logical_Layer.Viewport.screen_surface import Screen
from Logical_Layer.Entities.enemy import Enemy
from Logical_Layer.Util.limit import Limit
from Logical_Layer.Util.color import Color
from random import choice

class EnemiesGroup(sprite.Group):
    # Parameterized Constructor
    def __init__(self, enemyPosition: int, enemySpace: int, screen: Screen, columns: int, rows: int, horzVelocity : int):
        sprite.Group.__init__(self)
        self.enemies = [[None] * columns for _ in range(rows)]
        self.columns = columns
        self.rows = rows
        self.screen = screen
        self.width = self.screen.width
        self.collisionLimit = enemyPosition + (rows * enemySpace)    # The enemy's point where it will begin to collide with other entities
        self.verticalVelocity = 35
        self.horizontalVelocity = horzVelocity

        self._aliveColumns = list(range(columns))
        self._aliveRows = list(range(rows))  
        self._leftAliveColumn = 0
        self._rightAliveColumn = columns - 1
        self.moveTime = 600
        self.timer = time.get_ticks()
        self.horizMovement = True               # Horizontal Movement -> True: Move to the right | False: Move to the left
        self.vertMovement = False               # Vertical Movement -> True: Move down | False: Do not move down
        self.leftLimit = 25                     # The left boundary where the group must stop
        self.rightLimit = self.width - 25       # The right boundary where the group must stop

    # Overrides the Update method which is responsible for displaying elements on the screen
    def update(self, current_time):
        # Show vertical boundaries and horizontal collision boundary
        Limit.verticalBorders(self.screen, Color.YELLOW1, self.leftLimit, self.rightLimit)
        Limit.horizontalBorder(self.screen, Color.LIGHT_BLUE, self.collisionLimit)

        # Conditional that is true when the time is greather than moveTime (600) milliseconds. 
        # This conditional allows to refresh the enemy sprites to create a animation movement effect.
        if current_time - self.timer > self.moveTime:
            if self.vertMovement:                                    # Vertical movement
                # Toggle all sprites and move them down
                enemy : Enemy
                for enemy in self:
                    enemy.rect.y += self.verticalVelocity
                    enemy.toggle_image()

                # Determine the lower collision point
                numberSprites = len(self)
                if numberSprites > 0:
                    lastRowEnemy = self.sprites()[numberSprites - 1]
                    self.collisionLimit = lastRowEnemy.rect.bottom + self.verticalVelocity
                
                # Stop vertical movement
                self.vertMovement = False
            else:                                                   # Horizontal movement
                # Determines the direction of horizontal movement
                horzVelocity = self.horizontalVelocity if self.horizMovement else self.horizontalVelocity * -1
                for enemy in self:
                    enemy.rect.x += horzVelocity
                    enemy.toggle_image()

                # Check if the group reaches the right limit
                for row in self._aliveRows:
                    enemy = self.enemies[row][self._aliveColumns[-1]]
                    if enemy != None:
                        if enemy.rect.right > self.width:
                            raise Exception('The enemies are outside the width of the screen. Reduces the image size or the scaleFactor of the ImageScale instance.')
                
                        if enemy.rect.right >= self.rightLimit:
                            self.horizMovement = False  
                            self.vertMovement = True
                        break
                    
                # Check if the group reaches the left limit
                for row in self._aliveRows:
                    enemy = self.enemies[row][self._aliveColumns[0]]
                    if enemy != None:
                        if enemy.rect.left <= self.leftLimit:
                            self.horizMovement = True
                            self.vertMovement = True
                        break
                    
            # Update timer
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

    def is_column_dead(self, column: int):
        return not any(self.enemies[row][column]
                       for row in range(self.rows))

    def is_row_dead(self, row: int):
        return not any(self.enemies[row][column]
                        for column in range(self.columns))

    def kill(self, enemy: Enemy):
        self.enemies[enemy.row][enemy.column] = None
        is_column_dead = self.is_column_dead(enemy.column)
        is_row_dead = self.is_row_dead(enemy.row)

        if is_column_dead:
            self._aliveColumns.remove(enemy.column)

        if is_row_dead:
            self._aliveRows.remove(enemy.row)

        if enemy.column == self._rightAliveColumn:
            while self._rightAliveColumn > 0 and is_column_dead:
                self._rightAliveColumn -= 1
                is_column_dead = self.is_column_dead(self._rightAliveColumn)

        elif enemy.column == self._leftAliveColumn:
            while self._leftAliveColumn < self.columns and is_column_dead:
                self._leftAliveColumn += 1
                is_column_dead = self.is_column_dead(self._leftAliveColumn)
