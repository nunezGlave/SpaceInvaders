import spaceinvaders

# Class containing just the relevant data from the game
class observer:
    # SpaceInvaders Game will init this class at the start of game
    # Init AI class here
    def __init__(self, game_subject):
        # Subject is a reference to the SpaceInvaders Game class
        self.game_subject = game_subject
        # X position of the player
        self.player_x = 0
        # Number of enemies left in each column
        self.enemies_per_column = [0] * 11
        # X position of each bullet on the screen
        self.bullet_x = []
        # Average x position of all enemies on the screen
        self.average_enemy_x = 0
    # Called by the SpaceInvaders Game class every frame
    def update(self, player_x, enemies, bullets):
        self.player_x = player_x
        self.enemies_per_column = [0] * 11
        self.bullet_x = []
        for enemy in enemies:
            self.enemies_per_column[int(enemy.x/10)] += 1
            self.average_enemy_x += enemy.x
        self.average_enemy_x /= len(enemies)
        for bullet in bullets:
            self.bullet_x.append(bullet.x)
        self.print_update()
    # Returns the players x position relative to the screen width
    def get_player_screen_position(self):
        return self.player_x / self.game_subject.SCREEN_WIDTH
    # Returns the number of bullets within 50 pixels of the player
    def get_bullets_above_player(self):
        bullet_count = 0
        for bullet_x in self.bullet_x:
            if bullet_x > self.player_x-50 and bullet_x < self.player_x+50:
                bullet_count += 1
        return bullet_count
    # Print the current game state
    def print_update():
        str_out = ""
        str_out += "Player X: " + str(self.player_x) 
        for i in range(len(self.enemies_per_column)):
            str_out += "Col[" + str(i) + "]: " + str(self.enemies_per_column[i])
        str_out += "Avg X: " + str(self.average_enemy_x)
        str_out += "Bullets: " + str(self.bullet_x)
        print(str_out)
