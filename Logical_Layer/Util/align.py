from enum import Enum

class Align(Enum):
    LEFT = 1
    CENTER = 2
    RIGHT = 3

    @classmethod
    def horizontalAlignment(cls, align: Enum, xPos: float, textWidth: float):
        match align:
            case Align.RIGHT:
                return xPos
            case Align.CENTER:
                return xPos - (textWidth // 2)
            case Align.LEFT:
                return xPos - textWidth
            case _:
                return xPos
