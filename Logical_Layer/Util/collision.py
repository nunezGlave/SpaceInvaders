from pygame import *

class Collision():
    collision_rect = False

    @classmethod
    def detectionBorders(cls, rect: Rect, screen: Surface, color: tuple):
        if cls.collision_rect:
            border = rect.inflate(4, 4)            # Increase by 4 pixels on all sides for a border effect
            draw.rect(screen, color, border)       # Draw the edge of the rectangle
    