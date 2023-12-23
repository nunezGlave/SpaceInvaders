''' Created by Clark '''
from Logical_Layer.Interfaces.observer import Observer
from Logical_Layer.DQN.dqn import DQN
from pygame import *

class DQN_Observer(Observer):
    def __init__(self, game_instance):
        super().__init__(game_instance)
        self.playerDQN = DQN()

    # Update player DQN
    def update(self, score, enemies, bullets):
        self.playerDQN.update(
            self.player,
            score,
            self.player.ship, 
            enemies,
            self.get_player_bullets(self.player.bullets),
            self.get_enemy_bullets(bullets))
        self.playerDQN.request_action()

    def get_player_bullets(self, playerBullets : sprite.Group):
        bullets = []
        for bullet in playerBullets:
            bullets.append([bullet.rect.x, bullet.rect.y])
        return bullets

    def get_enemy_bullets(self, enemyBullets : sprite.Group):
        bullets = []
        for bullet in enemyBullets:
            bullets.append([bullet.rect.x, bullet.rect.y])
        return bullets
