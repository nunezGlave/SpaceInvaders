from pygame import *
from Logical_Layer.Entities.enemy import Enemy
from random import choice

class EnemiesGroup(sprite.Group):
    # Parameterized Constructor
    def __init__(self, enemyPosition: int, enemyMove: int, enemySize: int , width: int, columns: int, rows: int):
        sprite.Group.__init__(self)
        self.enemies = [[None] * columns for _ in range(rows)]
        self.columns = columns
        self.rows = rows
        self.width = width
        self.collisionVertLimit = enemyPosition + ((rows - 1) * (enemySize + 8)) + 35
        self.enemyMove = enemyMove

        self._aliveColumns = list(range(columns))
        self._aliveRows = list(range(rows))  
        self._leftAliveColumn = 0
        self._rightAliveColumn = columns - 1
        self.moveTime = 600
        self.timer = time.get_ticks()
        self.horizMovement = True            # Horizontal Movement -> True: Move to the right | False: Move to the left
        self.vertMovement = False            # Vertical Movement -> True: Move down | False: Don't move down
        self.horzLimit = 25                  # The horizontal limit where the group must stop

    # Overrides the Update method which is responsible for displaying elements on the screen
    def update(self, current_time):
        # Conditional that is true when the time is greather than moveTime (600) milliseconds. 
        # This conditional allows to refresh the enemy sprites to create a animation movement effect.
        if current_time - self.timer > self.moveTime:
            if self.vertMovement:
                # Toggle all sprites and move them down
                enemy : Enemy
                for enemy in self:
                    enemy.rect.y += self.enemyMove
                    enemy.toggle_image()

                # Determine the lower collision point
                numberSprites = len(self)
                if numberSprites > 0:
                    lastRowEnemy = self.sprites()[numberSprites - 1]
                    self.collisionVertLimit = lastRowEnemy.rect.bottom + self.enemyMove
                
                # Stop vertical movement
                self.vertMovement = False
            else:
                velocity = 10 if self.horizMovement else -10
                for enemy in self:
                    enemy.rect.x += velocity
                    enemy.toggle_image()

                # Check if the group reaches the right limit
                for row in self._aliveRows:
                    enemy = self.enemies[row][self._aliveColumns[-1]]
                    if enemy != None:
                        if enemy.rect.x >= (self.width - enemy.size - self.horzLimit):
                            self.horizMovement = False  
                            self.vertMovement = True
                        break

                # Check if the group reaches the left limit
                for row in self._aliveRows:
                    enemy = self.enemies[row][self._aliveColumns[0]]
                    if enemy != None:
                        if enemy.rect.x <= self.horzLimit:
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
