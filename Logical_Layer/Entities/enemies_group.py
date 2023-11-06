from pygame import *
from Logical_Layer.Entities.enemy import Enemy
from random import choice

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
                enemy : Enemy
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

    def is_column_dead(self, column: int):
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

    def kill(self, enemy: Enemy):
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
