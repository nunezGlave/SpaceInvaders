from Logical_Layer.Interfaces.scale import Scale
import pygame
from pygame.locals import *
from pygame import *

class TextScale(Scale):
    def __init__(self, scaleType: int, size: int, scaleFactor: float = 0.86):
        super().__init__(scaleType)
        self.scaleFactor = 0.86  if scaleFactor > 1 or scaleFactor < 0.6 else scaleFactor
        self.originalSize = size
        self.scaleSize = self.newSize()
        
    def newSize(self):
        match super().scaleNumber:
            case 2:
                newSize = self.originalSize * self.scaleFactor        # scaleFactor reduces the size by a given percentage
            case 3:
                secondSize = self.originalSize * self.scaleFactor     # Second type's size
                newSize = secondSize * self.scaleFactor               # A percentage less than the second type's size
            case _:
                newSize = self.originalSize               # type 1 or unspecified remains the same size
        
        return int(newSize)
    
    @classmethod 
    def scaleWidth(cls, text: str, textFont: str, letterSize: int):
        font = pygame.font.Font(textFont, letterSize)
        surface : Surface = font.render(text, True, (255, 255, 255))
        return surface.get_width()
    
