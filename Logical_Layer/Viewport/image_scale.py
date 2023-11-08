from Logical_Layer.Interfaces.scale import Scale
from pygame import *

class ImageScale(Scale):
    def __init__(self, scaleType: int, image, size: int):
        super().__init__(scaleType)
        self.originalSize = size
        self.originalImage = image
        self.scaleSize = self.newSize()
        self.scaleImage = self.newImage() if type(image) is not dict else None
        # print("newSize: ", self.scaleSize)
        # print("scaleImage: ", self.scaleImage)

    def newSize(self):
        match super().scaleNumber:
            case 2:
                newSize = self.originalSize * 0.7         # 20% less than the original size
            case 3:
                sizeType2 = self.originalSize * 0.7       # 20% less than the original size
                newSize = sizeType2 * 0.8                 # 20% less than the second type's size
            case _:
                newSize = self.originalSize               # type 1 or unspecified remains the same size
        
        return int(newSize)

    def newImage(self):
        return self.scale(self.originalImage, self.scaleSize, self.scaleSize)
    
    @classmethod
    def scale(cls, image: Surface, wSize: int, hSize: int):
        return transform.scale(image, (wSize, hSize))
