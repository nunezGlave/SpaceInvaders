''' Created by Clark '''
from Logical_Layer.Interfaces.observer import Observer
from Logical_Layer.A3C import Space_bot

class A3C_Observer(Observer):
    def __init__(self, game_instance):
        super().__init__(game_instance)
        self.player_x = 0
        self.enemies_per_column = [0] * 11
        self.bullet_x = []
        self.average_enemy_x = 0
        self.Space_bot = Space_bot.space_bot(3,3,self)
        self.Space_bot.set_inputs([0.0] * 3)
        self.Space_bot.set_layers()

    def update(self):
        self.player_x = self.game_instance.player.rect.x
        self.enemies_per_column = [0] * 11
        self.bullet_x = []
        for enemy in self.game_instance.enemies:
            self.enemies_per_column[enemy.column] += 1
            self.average_enemy_x += enemy.rect.x
        if len(self.game_instance.enemies) > 0:
            self.average_enemy_x /= len(self.game_instance.enemies)
        for bullet in self.game_instance.bullets:
            self.bullet_x.append(bullet.rect.x)
        self.Space_bot.choose_move([self.get_player_screen_position(), self.get_bullets_above_player(), self.average_enemy_x / self.game_instance.screen.get_width()])
       # self.print_update()

    def get_player_screen_position(self):
        return self.player_x / self.game_instance.screen.get_width()

    def get_bullets_above_player(self):
        bullet_count = 0
        for bullet_x in self.bullet_x:
            if self.player_x - 50 < bullet_x < self.player_x + 50:
                bullet_count += 1
        return bullet_count

    def print_update(self):
        str_out = ""
        str_out += "Player X: " + str(self.player_x)
        for i in range(len(self.enemies_per_column)):
            str_out += "Col[" + str(i) + "]: " + str(self.enemies_per_column[i])
        str_out += "Avg X: " + str(self.average_enemy_x)
        str_out += "Bullets: " + str(self.bullet_x)
        print(str_out)

