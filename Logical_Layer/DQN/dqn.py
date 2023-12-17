import numpy as np
import random
import pygame


class Human:
    def __init__(self, game_instance):
        self.game_instance = game_instance
        self.enemies = self.game_instance.enemies
        self.player = self.game_instance.player
        self.player_bullets = self.game_instance.bullets
        self.enemy_bullets = self.game_instance.enemyBullets

    def update(self, player_x, enemies, bullets, enemy_bullets):
        self.enemies = enemies.return_enemy()
        self.player = player_x
        self.bullets = bullets
        self.enemy_bullets = enemy_bullets
        self.keys = pygame.key.get_pressed()
        if self.keys[pygame.K_LEFT]:
            self.send_command("left")
        if self.keys[pygame.K_RIGHT]:
            self.send_command("right")
        if self.keys[pygame.K_SPACE]:
            self.send_command("shoot")

    def send_command(self, command):
        self.game_instance.command(command)


class DQN:
    def __init__(self):
        self.game_instance = None
        self.enemies = None
        self.player = None
        self.bullets = None
        self.enemy_bullets = None
        self.keys = None
        self.score = 0
        self.q_table = {}
        self.alpha = 0.01
        self.gamma = 0.95
        self.action_size = 2  
        self.reward = 0
    def update(self, game_instance, score, player, enemies, bullets_xy, enemy_bullets_xy):
        self.game_instance = game_instance
        self.enemies = enemies.return_enemy()
        self.player = player.rect.x
        self.bullets = bullets_xy
        self.enemy_bullets = enemy_bullets_xy
        self.keys = pygame.key.get_pressed()
        self.score = score
        

################################################################################
    def request_action(self):
        current_state = self.get_current_state()

        if current_state not in self.q_table:
            self.q_table[current_state] = np.zeros([self.action_size])

        epsilon = 0.2  # Exploration probability
        if random.random() < epsilon:
            action = random.randint(0, self.action_size - 1)
        else:
            action = np.argmax(self.q_table[current_state])

        # Execute the chosen action
        if action == 0:
            self.shoot_left_or_right()
        elif action == 1:
            self.shoot_right_or_left()
        else:
            print("Invalid action")

        # Update rewards based on the game state
        reward = self.calculate_reward(current_state, action)

        # Learn and update Q-values based on the observed reward
        self.learn(current_state, action, reward)

    def shoot_left_or_right(self):
        if random.random() < 0.5:
            self.send_command("shoot")
            self.send_command("left")
            print("shoot left")
        else:
            self.send_command("shoot")
            self.send_command("right")
            print("shoot right")

    def shoot_right_or_left(self):
        if random.random() < 0.5:
            self.send_command("shoot")
            self.send_command("right")
            print("shoot right")
        else:
            self.send_command("shoot")
            self.send_command("left")
            print("shoot left")
################################################################################

    #def calculate_reward(self, current_state, action):
    #   return self.reward

    def calculate_reward(self, current_state, action):
    # check if player bullet hits a wall
        for bullet_x, bullet_y in self.bullets:
            if bullet_y > 800 or bullet_y < 450:  # screen height 800 and collision with blockers
                # penalize for hitting the roof, hitting blockers, and letting enemies getting close.
                return self.reward - 1

        return self.reward
    
    def should_avoid_enemy_bullets(self):
        for bullet_x, bullet_y in self.enemy_bullets:
            if abs(bullet_y - self.player) < 10:
                return True
        return False

    def avoid_enemy_bullets_action(self):
        left_bullets = [(bullet_x, bullet_y) for bullet_x,
                        bullet_y in self.enemy_bullets if bullet_x < self.player]
        right_bullets = [(bullet_x, bullet_y) for bullet_x,
                         bullet_y in self.enemy_bullets if bullet_x > self.player]

        if left_bullets:
            left_dist = min([abs(bullet_x - self.player)
                            for bullet_x, _ in left_bullets])
        else:
            left_dist = float('inf')

        if right_bullets:
            right_dist = min([abs(bullet_x - self.player)
                             for bullet_x, _ in right_bullets])
        else:
            right_dist = float('inf')

        if left_dist < right_dist:
            return 0  # Move left
        else:
            return 1  # Move right

    def move_towards_nearest_enemy(self):
        nearest_enemy = self.find_nearest_enemy()
        if nearest_enemy is not None:
            nearest_enemy_x = nearest_enemy[0]
            if nearest_enemy_x < self.player:
                self.send_command("left")
            else:
                self.send_command("right")

    def find_nearest_enemy(self):
        if not self.enemies:
            return None
        nearest_enemy = min(self.enemies, key=lambda enemy_pos: abs(
            enemy_pos[0] - self.player))
        return nearest_enemy

    def send_command(self, command):
        self.game_instance.command(command)

    def learn(self, current_state, action, reward):
        if current_state not in self.q_table:
            self.q_table[current_state] = np.zeros([self.action_size])

        # Q-learning update rule
        self.q_table[current_state][action] = (1 - self.alpha) * self.q_table[current_state][action] + \
            self.alpha * (reward + self.gamma * np.max(self.q_table[current_state]))

    def get_current_state(self):
        enemies_state = tuple(tuple(coords) for coords in self.enemies)
        bullets_state = tuple(tuple(coords) for coords in self.bullets)
        enemy_bullets_state = tuple(tuple(coords)
                                    for coords in self.enemy_bullets)

        return (self.player, enemies_state, bullets_state, enemy_bullets_state, self.score)
