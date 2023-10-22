import pygame


class Human:
    def __init__(self, game_instance):
        self.game_instance = game_instance

    def send_command(self, command):
        self.game_instance.command(command)

    def update(self, player_x, enemies, bullets):
        self.keys = pygame.key.get_pressed()
        if self.keys[pygame.K_LEFT]:
            self.send_command("left")
        if self.keys[pygame.K_RIGHT]:
            self.send_command("right")
        if self.keys[pygame.K_SPACE]:
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