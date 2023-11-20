from Logical_Layer.Interfaces.viewport import Viewport
from Presentation_Layer.introduction_menu import IntroductionMenu
from Presentation_Layer.difficulty_menu import DifficultyMenu

class GameController(Viewport):
    def __init__(self):
        super().__init__("Game Controller")
        self.current_state = IntroductionMenu()

    def draw(self):
        self.current_state.draw()

    def handle_events(self, events):
        action = self.current_state.handle_events(events)
        if action == 'switch_to_introduction':
            self.switch_state(IntroductionMenu())
        elif action == 'switch_to_difficulty':
            self.switch_state(DifficultyMenu())

    def switch_state(self, new_state):
        self.current_state = new_state

