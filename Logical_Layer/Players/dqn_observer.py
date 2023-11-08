''' Created by Clark '''
from Logical_Layer.Interfaces.observer import Observer

class DQN_Observer(Observer):
    def __init__(self, game_instance):
        super().__init__(game_instance)
        self.player_x = 0
        self.enemies_per_column = [0] * 11
        self.bullet_x = []
        self.average_enemy_x = 0

    def update(self, player_x, enemies, bullets):
        self.player_x = player_x
        self.enemies_per_column = [0] * 11
        self.bullet_x = []
        for enemy in enemies:
            self.enemies_per_column[int(enemy.x / 10)] += 1
            self.average_enemy_x += enemy.x
        self.average_enemy_x /= len(enemies)
        for bullet in bullets:
            self.bullet_x.append(bullet.x)
        self.print_update()


