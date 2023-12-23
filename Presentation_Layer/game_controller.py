from Logical_Layer.Interfaces.viewport import Viewport
from Logical_Layer.Util.state import State
from Presentation_Layer.introduction_menu import IntroductionMenu
from Presentation_Layer.difficulty_menu import DifficultyMenu
from Presentation_Layer.player_menu import PlayerMenu
from Presentation_Layer.game import SpaceInvaders
from Presentation_Layer.scoreboard import Scoreboard
from Presentation_Layer.guide_menu import GuideMenu
from pygame import *

class GameController(Viewport):
    def __init__(self):
        super().__init__("Game Controller")

        # Load the icon image
        icon = image.load('{}/{}'.format(self.imagePath, 'logo1.jpg'))

        # Set the Pygame window icon
        display.set_icon(icon)

        # Reproduce main sound
        self.mainSound.play(-1)

        # Start the game
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
            self.checkMainSound()
            match action['state'].value:
                case State.INTRO.value:
                    self.switch_state(IntroductionMenu())
                case State.DIFFICULTY.value:
                    self.switch_state(DifficultyMenu())
                case State.PLAYER.value:
                    difficulty = action['difficulty']
                    if action.get('restart') is not None:
                        self.secondaryState = None
                    self.switch_state(PlayerMenu(difficulty))
                case State.GAME.value:
                    self.mainSound.stop()
                    modeGame = action['mode-game']
                    difficulty = action['difficulty']
                    if modeGame == 1:
                        player = action['player']
                        self.switch_state(SpaceInvaders(modeGame, player, difficulty, self.display.width, self.display.height))
                    elif modeGame == 2:
                        team1 = action['team-left']
                        team2 = action['team-right']
                        spLeft = SpaceInvaders(modeGame, team1, difficulty, self.display.halfWidth, self.display.height, 0 , 0)
                        spRight = SpaceInvaders(modeGame, team2, difficulty, self.display.halfWidth, self.display.height, self.display.halfWidth, 0)
                        self.switch_state(spLeft, spRight)
                case State.SCORE.value:
                    difficulty = action['difficulty']
                    self.switch_state(Scoreboard(difficulty))
                case State.GUIDE.value:
                    difficulty = action['difficulty']
                    modeGame = action['mode-game']
                    self.switch_state(GuideMenu(difficulty, modeGame))
                case _:
                    pass

    def switch_state(self, new_state, new2_state = None):
        if self.mainState != None:
            self.mainState = new_state
        
        if new2_state != None:
            self.secondaryState = new2_state

    def checkMainSound(self):
        if mixer.get_busy() == False:
            self.mainSound.play(-1)


