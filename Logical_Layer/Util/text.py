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

        # Text width and height
        self.textWidth =  self.surface.get_width()
        self.textHeight = self.surface.get_height()

        # The union of the position of the text and its size in pixels.
        self.widthPosX =  self.xPos + self.textWidth
        self.heightPosY = self.yPos + self.textHeight

    # Draw text
    def draw(self, screen: Surface):
        screen.blit(self.surface, self.rect)

    # Flip text
    def rotate(self, angle: float):
        self.surface = transform.rotate(self.surface, angle)

