# No Yet implemented
from Logical_Layer.Interfaces.scale import Scale

class PositionScale(Scale):
    def __init__(self, scaleType, size, position):
        super().__init__(scaleType)
        self.position = position

    def newSize(self):
        print("Not yet implemented")
