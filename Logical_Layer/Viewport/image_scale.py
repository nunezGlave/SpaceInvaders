from Logical_Layer.Interfaces.scale import Scale
from pygame import *

class ImageScale(Scale):
    def __init__(self, scaleType: int, image: Surface, sizeWidth: int, sizeHeight: int, scaleFactor : float = 0.75): 
        super().__init__(scaleType)
        self.scaleFactor = 0.75 if scaleFactor > 1 or scaleFactor < 0.6 else scaleFactor
        self.givenImage = image             
        self.originalWidth = sizeWidth          
        self.originalHeight = sizeHeight
        self.scaleWidth = self.newSize(sizeWidth)  
        self.scaleHeight = self.newSize(sizeHeight)    
        self.scaleImage = self.newImage()
        
    def newSize(self, size: int):
        match super().scaleNumber:
            case 2:
                newSize = size * self.scaleFactor         # scaleFactor reduces the size by a given percentage
            case 3:
                secondSize = size * self.scaleFactor      # Second type's size
                newSize = secondSize * self.scaleFactor   # A percentage less than the second type's size
            case _:
                newSize = size                       # type 1 or unspecified remains the same size
        
        return int(newSize)

    def newImage(self):
        return transform.scale(self.givenImage, (self.scaleWidth, self.scaleHeight))