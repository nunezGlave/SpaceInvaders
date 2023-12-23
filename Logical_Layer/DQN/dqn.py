class DQN:
    def __init__(self):
        self.playerControl = None
        self.enemies = None
        self.player = None
        self.bullets = None
        self.enemy_bullets = None
        self.keys = None
        self.score = 0
        self.q_table = {}

        self.alpha = 0.1
        self.gamma = 0.9

        self.action_size = 2


    def update(self, game_instance, score, player, enemies, bullets_xy, enemy_bullets_xy):
        self.game_instance = game_instance
        self.enemies = enemies.return_enemy()
        self.player = player.rect.x
        self.bullets = player_bullets_xy
        self.enemy_bullets = enemy_bullets_xy
        self.keys = pygame.key.get_pressed()
        self.score = score

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
        elif action == 1:
            print("shoot right")
            self.send_command("right")
            self.send_command("shoot")
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
        self.playerControl.command(command)

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
