from enum import Enum

class State(Enum):
    DIFFICULTY = 'switch_to_difficulty'
    INTRO = 'switch_to_introduction'
    PLAYER = 'switch_to_player'
    GAME = 'switch_to_game'
    SCORE = 'switch_to_scoreboard'
