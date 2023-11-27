from Logical_Layer.Interfaces.viewport import Viewport
from Logical_Layer.Util.state import State
from Presentation_Layer.introduction_menu import IntroductionMenu
from Presentation_Layer.difficulty_menu import DifficultyMenu
from Presentation_Layer.player_menu import PlayerMenu
from Presentation_Layer.game import SpaceInvaders
from Presentation_Layer.scoreboard import Scoreboard

class GameController(Viewport):
    def __init__(self):
        super().__init__("Game Controller")
        self.mainState = IntroductionMenu()
        self.secondaryState : Viewport = None

    def draw(self):
        if self.mainState != None:
            self.mainState.draw()

        if self.secondaryState != None:
            self.secondaryState.draw()

    def handle_events(self, events):
        # Get current status
        action = self.mainState.handle_events(events)

        # Change status
        if action != None:
            match action['state'].value:
                case State.INTRO.value:
                    self.switch_state(IntroductionMenu())
                case State.DIFFICULTY.value:
                    self.switch_state(DifficultyMenu())
                case State.PLAYER.value:
                    difficulty = action['difficulty']
                    self.switch_state(PlayerMenu(difficulty))
                case State.GAME.value:
                    modeGame = action['mode-game']
                    difficulty = action['difficulty']
                    if modeGame == 1:
                        player = action['player']
                        self.switch_state(SpaceInvaders(modeGame, player, difficulty, self.display.width, self.display.height))
                    elif modeGame == 2:
                        player1 = action['player1']
                        player2 = action['player2']
                        spLeft = SpaceInvaders(modeGame, player1, difficulty, self.display.halfWidth, self.display.height, 0 , 0)
                        spRight = SpaceInvaders(modeGame, player2, difficulty, self.display.halfWidth, self.display.height, self.display.halfWidth, 0)
                        self.switch_state(spLeft, spRight)
                case State.SCORE.value:
                    difficulty = action['difficulty']
                    self.switch_state(Scoreboard(difficulty))
                case _:
                    pass

    def switch_state(self, new_state, new2_state = None):
        if self.mainState != None:
            self.mainState = new_state
        
        if new2_state != None:
            self.secondaryState = new2_state

