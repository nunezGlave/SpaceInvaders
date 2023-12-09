''' Created by Clark '''
import random

from Logical_Layer.Interfaces.observer import Observer
from Logical_Layer.A3C import Space_bot

class A3C_Observer(Observer):
    def __init__(self, game_instance):
        super().__init__(game_instance)
        self.player_x = 0
        self.bullet_x = []
        self.space_bot = Space_bot.Space_bot(3, 3, self)
        self.space_bot.set_inputs([0.0] * 3)
        self.space_bot.set_layers()
        self.average_enemy_x = 0
        self.space_bot.import_bot()
        self.start = True
    def update(self, px, enemies, bullets):
        self.player_x = self.game_instance.player.rect.x
        self.bullet_x = []
        self.space_bot.score = self.game_instance.score
        for enemy in self.game_instance.enemies:
            self.average_enemy_x += enemy.rect.x
        self.average_enemy_x /= len(self.game_instance.enemies)+1
        for bullet in self.game_instance.enemyBullets:
            self.bullet_x.append(bullet.rect.x)
        self.space_bot.choose_move([self.get_player_screen_position(), self.get_bullets_above_player(), self.get_average_enemy_x()])
       # self.print_update()

    def get_player_screen_position(self):
        return (self.player_x*2 -self.game_instance.displaySub.width/2)/(self.game_instance.displaySub.width/2)* random.uniform(0.5,1.5)

    def get_bullets_above_player(self):
        bullet_count = 0
        for bullet_x in self.bullet_x:
            if self.player_x - 50 < bullet_x:
                bullet_count -= 15
            elif bullet_x < self.player_x + 50:
                bullet_count += 15
        return bullet_count
    def get_enemy_count(self):
        return len(self.game_instance.enemies)-25
    def get_average_enemy_x(self):
        return ((self.average_enemy_x-self.game_instance.displaySub.width/2)/(self.game_instance.displaySub.width/2) - self.get_player_screen_position())
    def print_update(self):
        str_out = ""
        str_out += "Player X: " + str(self.player_x)
        for i in range(len(self.enemies_per_column)):
            str_out += "Col[" + str(i) + "]: " + str(self.enemies_per_column[i])
        str_out += "Avg X: " + str(self.average_enemy_x)
        str_out += "Bullets: " + str(self.bullet_x)
        print(str_out)
    def end_game(self,score):
        pass
        # self.space_bot.end_game(score)
    def send_command(self, command):
        self.game_instance.command(command)