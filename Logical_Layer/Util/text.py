from pygame import *
from Logical_Layer.Util.align import Align
from Logical_Layer.Util.color import Color

class Text(object):
    # Parameterized Constructor
    def __init__(self, message: str, textFont: str, letterSize: int, color: Color, xPos: float , yPos: float, align: Align = Align.RIGHT):
        self.font = font.Font(textFont, letterSize)
        self.surface = self.font.render(message, True, color.value)
        self.size = letterSize
        
        # Align horizontally based on the given x-axis position 
        xPos = Align.horizontalAlignment(align, xPos, self.surface.get_width())
        self.rect = self.surface.get_rect(topleft=(xPos, yPos))

        # Vertical and horizontal position of the text
        self.xPos, self.yPos = xPos, yPos

        # The union of the position of the text and its size in pixels.
        self.textWidth =  self.xPos + self.surface.get_width()
        self.textHeight = self.yPos + self.surface.get_height()

    def draw(self, surface: Surface):
        surface.blit(self.surface, self.rect)
