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

        self.alpha = 0.1
        self.gamma = 0.9

        self.action_size = 2


    def update(self, game_instance, score, player, enemies, bullets_xy, enemy_bullets_xy):
        self.game_instance = game_instance
        self.enemies = enemies.return_enemy()
        self.player = player.rect.x
        self.bullets = bullets_xy
        self.enemy_bullets = enemy_bullets_xy
        self.keys = pygame.key.get_pressed()
        self.score = score

    def request_action(self):
        current_state = self.get_current_state()
        if current_state not in self.q_table:
            self.q_table[current_state] = np.zeros([self.action_size])

        if random.random() < 0.3:
            action = random.randint(0, self.action_size - 1)
        else:
            action = np.argmax(self.q_table[current_state])

        if action == 0:
            self.send_command("shoot")
            self.send_command("left")
            print("shoot left")
        elif action == 1:
            print("shoot right")
            self.send_command("right")
            self.send_command("shoot")
        else:
            print("Invalid action")
    def send_command(self, command):
        self.game_instance.command(command)

    def learn(self):
        current_state = self.get_current_state()
        action = self.request_action(0)
        next_state, reward = self.game_instance.step(action)

        if next_state not in self.q_table:
            self.q_table[next_state] = np.zeros([self.action_size])

        self.q_table[current_state][action] = (1 - self.alpha) * self.q_table[current_state][action] + \
            self.alpha * (reward + self.gamma *
                          np.max(self.q_table[next_state]))

    def get_current_state(self):
        enemies_state = tuple(tuple(coords) for coords in self.enemies)
        bullets_state = tuple(tuple(coords) for coords in self.bullets)
        enemy_bullets_state = tuple(tuple(coords) for coords in self.enemy_bullets)

        return (self.player, enemies_state, bullets_state, enemy_bullets_state, self.score)

