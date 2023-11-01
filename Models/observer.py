'''
    Created by Clark
'''
import pygame

class observer_interface:
    def __init__(self, game_instance):
        self.game_instance = game_instance

    def update(self, player_x, enemies, bullets):
        pass
    
    def send_command(self, command):
        self.game_instance.command(command)

class human_observer(observer_interface):
    def __init__(self, game_instance, player_index):
        super().__init__(game_instance)
        self.player_index = player_index

    def update(self, player_x, enemies, bullets):
        self.keys = pygame.key.get_pressed()
        if self.player_index == 0:
            if self.keys[pygame.K_LEFT]:
                self.send_command("left")
            if self.keys[pygame.K_RIGHT]:
                self.send_command("right")
            if self.keys[pygame.K_SPACE]:
                self.send_command("shoot")
        elif self.player_index == 1:
            if self.keys[pygame.K_a]:
                self.send_command("left")
            if self.keys[pygame.K_d]:
                self.send_command("right")
            if self.keys[pygame.K_w]:
                self.send_command("shoot")


class A3C_observer(observer_interface):
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

    def get_player_screen_position(self):
        return self.player_x / self.game_subject.SCREEN_WIDTH

    def get_bullets_above_player(self):
        bullet_count = 0
        for bullet_x in self.bullet_x:
            if bullet_x > self.player_x - 50 and bullet_x < self.player_x + 50:
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


class DQN_observer(observer_interface):
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


