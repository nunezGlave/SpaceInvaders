from pygame import Surface

class Screen():
    def __init__(self, gameScreen: Surface):
        self.surface = gameScreen
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()
        self.halfWidth = self.width / 2
        self.halfHeight = self.height / 2

    def widthP(self, percentage: float):
        if (percentage >= 0 and percentage <= 100):
            screenPer = self.width * (percentage / 100)
            return int(screenPer)
        else:
            raise Exception("The screen percentage must be between 0 and 100.")
    
    def heightP(self, percentage: float):
        if (percentage >= 0 and percentage <= 100):
            screenPer = self.height * (percentage / 100)
            return int(screenPer)
        else:
            raise Exception("The screen percentage must be between 0 and 100.")
    