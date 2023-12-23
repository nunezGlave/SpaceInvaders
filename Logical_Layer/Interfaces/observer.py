class Observer:
    def __init__(self, player):
        self.player = player

    def update(self, score, enemies, bullets):
        pass
    
    def send_command(self, command):
        self.player.command(command)
    
    def end_game(self,score):
        pass