from pygame import *
from Logical_Layer.Util.color import Color
from Logical_Layer.Viewport.screen_surface import Screen

class Limit():
    _collision_rect = False
    _collision_borders = False

    @classmethod
    def verticalBorders(cls, screen: Screen, color: Color, leftPos: int, rightPos : int):
        if cls._collision_borders:
            draw.line(screen.surface, color.value, (leftPos, 0), (leftPos, screen.height), 2)
            draw.line(screen.surface, color.value, (rightPos, 0), (rightPos, screen.height), 2)

    @classmethod
    def horizontalBorder(cls, screen: Screen, color: Color, yPos: int):
        if cls._collision_borders:
            draw.line(screen.surface, color.value, (0, yPos), (screen.width, yPos), 2)

    @classmethod
    def bordersCollision(cls, rect: Rect, screen: Surface, color: Color):
        if cls._collision_rect:
            border = rect.inflate(4, 4)                  # Increase by 4 pixels on all sides for a border effect
            draw.rect(screen, color.value, border)       # Draw the edge of the rectangle
    