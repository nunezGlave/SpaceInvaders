

class Observer:
    def __init__(self, game_instance):
        self.game_instance = game_instance

    def update(self, player_x, enemies, bullets):
        pass
    
    def send_command(self, command):
        self.game_instance.command(command)
