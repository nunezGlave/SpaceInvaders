from Logical_Layer.Interfaces.scale import Scale
import pygame
from pygame.locals import *
from pygame import *

class TextScale(Scale):
    def __init__(self, scaleType: int, size: int):
        super().__init__(scaleType)
        self.originalSize = size
        self.scaleSize = self.newSize()
        

    def newSize(self):
        match super().scaleNumber:
            case 2:
                newSize = self.originalSize * 0.86        # 14% less than the original size
            case 3:
                sizeType2 = self.originalSize * 0.86      # 14% less than the original size
                newSize = sizeType2 * 0.86                # 14% less than the second type's size
            case _:
                newSize = self.originalSize               # type 1 or unspecified remains the same size
        
        return int(newSize)
    
    @classmethod 
    def scaleWidth(cls, text: str, textFont: str, letterSize: int):
        
        font = pygame.font.Font(textFont, letterSize)
        surface : Surface = font.render(text, True, (255, 255, 255))
        return surface.get_width()
    
