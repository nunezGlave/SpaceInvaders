

run SpaceInvaders.py


really important: 
                    self.dqn = self.playerDQN
                    self.dqn.update(
                        self,
                        self.score,
                        self.player, 
                        self.enemies,
                        self.get_player_bullets(),
                        self.get_enemy_bullets())
                    self.dqn.request_action()