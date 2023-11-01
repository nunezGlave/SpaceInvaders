import pygame


class Human:
    def __init__(self, game_instance):
        self.game_instance = game_instance

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
class DQN:
    def __init__(self, game_instance):
        self.game_instance = game_instance

    def send_command(self, command):
        self.game_instance.command(command)

    def update(self, player_x, enemies, bullets):
        pass

class A3C:
    def __init__(self, game_instance):
        self.game_instance = game_instance

    def send_command(self, command):
        self.game_instance.command(command)

    def update(self, player_x, enemies, bullets):
        pass