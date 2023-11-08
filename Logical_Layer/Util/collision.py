from pygame import *
from Logical_Layer.Util.color import Color

class Collision():
    collision_rect = True

    @classmethod
    def detectionBorders(cls, rect: Rect, screen: Surface, color: Color):
        if cls.collision_rect:
            border = rect.inflate(4, 4)                  # Increase by 4 pixels on all sides for a border effect
            draw.rect(screen, color.value, border)       # Draw the edge of the rectangle
    