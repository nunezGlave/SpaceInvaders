from pygame import *
from Logical_Layer.Util.color import Color
import pygame as py

class Image():
    # Parameterized Constructor
    def __init__(self, screen: Surface, image : Surface, width: float, height: float = 0):
        # Scale image and its dimension
        self.image = transform.scale(image, (int(width), int(width if height == 0 else height)))
        self.rect = self.image.get_rect()
        
        # Set screen
        self.screen = screen

        # Event controller
        self.clicked = False
        
    # Flip image
    def flip(self, flipX: bool, flipY : bool):
        self.image = transform.flip(self.image, flipX, flipY)

    # Draw image
    def draw(self, posX : int, posY : int):
        # Get the new position of the image
        self.rect = self.image.get_rect(topleft = (posX, posY))
        
        # Draw the surface
        self.screen.blit(self.image, self.rect)

	# Draw a circle around the image
    def drawCircle(self,  posX : int, posY : int, outerColor: Color, innerColor: Color):
        # Inner and outer radious
        self.outerRadious = max(self.rect.width, self.rect.height) * 0.85
        self.innerRadious = self.outerRadious * 0.85

        # Get attributes
        circlePosition = (posX, posY)
        self.outerColor = outerColor.value
        self.innerColor = innerColor.value

        # Draw outer circle
        self.outerCircle = draw.circle(self.screen, self.outerColor, circlePosition, self.outerRadious)

        # Draw inner circle
        self.innerCircle = draw.circle(self.screen, self.innerColor, circlePosition, self.innerRadious)
            
        # Center the image and draw it
        self.rect = self.image.get_rect(center=circlePosition)
        self.screen.blit(self.image, self.rect)

	# Draw a rectangle with text below the circle
    def drawBox(self, textBox: str, fontBox: str, leftSide: Surface = None, rightSide: Surface = None, showLeftArrow : bool = True, showRightArrow : bool = True):
        if hasattr(self, 'innerCircle'):
           # Get text
           self.id = textBox[0]
           self.name = textBox[1]

           # Size of the outer and inner rectangle
           outerWidth = self.rect.width * 1.7
           outerHeight = self.rect.height * 0.54
           innerWidth = outerWidth * 0.9
           innerHeight = outerHeight * 0.78
           
           # Border radious
           borderRadious = 50
           
           # Points of the outer rectangle
           outerPosX = self.innerCircle.left + (self.innerCircle.width - outerWidth) // 2
           outerPosY = self.innerCircle.bottom
           
           # Create and draw outer rectangle
           self.outerRect = Rect(outerPosX, outerPosY, outerWidth, outerHeight)
           self.outerBox = draw.rect(self.screen, self.innerColor, self.outerRect, border_radius=borderRadious)
           
           # Points of the inner rectangle
           innerPosX = self.outerRect.x + 0.5 + (outerWidth -  innerWidth) / 2 
           innerPosY = self.outerRect.y + 0.5 + (outerHeight -  innerHeight) / 2 
           
           # Create and draw inner rectangle
           self.innerRect = Rect(innerPosX, innerPosY, innerWidth, innerHeight)
           self.innerBox = draw.rect(self.screen, self.outerColor, self.innerRect, border_radius=borderRadious)
           
           # Resize text
           self.text = self._resizeText(self.outerRect, fontBox, self.name, 0.71)
           
           # Center text and draw it
           self.textRect = self.text.get_rect(center= self.innerBox.center)
           self.screen.blit(self.text, self.textRect)
           
		   # Draw side's left
           if leftSide != None and showLeftArrow:
               if isinstance(leftSide, Surface):
                  leftX = self.rect.x - (self.outerCircle.width / 2) - 8
                  result = self._drawSides(leftSide, leftX, self.innerCircle)
                  self.leftRect : Rect = result['rect']
                  self.leftImage : Surface = result['image']
                  
		   # Draw side's right
           if rightSide != None and showRightArrow:
               if isinstance(rightSide, Surface):
                  rightX = self.outerCircle.right + 8
                  result = self._drawSides(rightSide, rightX, self.innerCircle)
                  self.rightRect : Rect = result['rect']
                  self.rightImage : Surface = result['image']

        else:
           print('You need to call drawCircle first to create the drawBox')

	# Evaluate which side was pressed
    def sidesClick(self):
        if hasattr(self, 'leftImage'):
           if self._mouseClick(self.leftRect):
               return 'LEFT'
           
        if hasattr(self, 'rightImage'):
           if self._mouseClick(self.rightRect):
               return 'RIGHT'
           
        return 'NONE'
           
	# Draw images on the sides
    def _drawSides(self, imageSide : Surface, xPos : float, yPos : Rect):
		# Get image's width and height
        sidesWidth = imageSide.get_width()
        sidesHeigth = imageSide.get_height()
                
        # Calculate image's scale
        scale = (self.innerCircle.height * 0.40) / 100
        
        # Scale image
        imageSide = transform.scale(imageSide, (int(sidesWidth * scale), int(sidesHeigth * scale)))
        
        # Calculate position on the y-axis
        yPos = self.innerCircle.y + (self.innerCircle.height - imageSide.get_height()) / 2

        # Draw side
        sideRect = imageSide.get_rect(topleft = (xPos, yPos))
        self.screen.blit(imageSide, sideRect)
        
		# Return side
        return {'image' : imageSide, 'rect' : sideRect}

    # Capture click event
    def _mouseClick(self, rect: Rect) -> bool:
        action = False
        # Get mouse position
        pos = mouse.get_pos()

        # Check mouseover and clicked conditions
        if rect.collidepoint(pos):
            if mouse.get_pressed()[0] and self.clicked == False:
                self.clicked = True
                action = True
            
        if mouse.get_pressed()[0]:
            self.clicked = False

        return action
    
    # Resize font size
    def _resizeText(self, recc : Rect, fontBox, textBox, size) -> Surface:
        # Initial text rendering
        startFontSize = 1000
        font = py.font.Font(fontBox, startFontSize)
        text : Surface = font.render(textBox, True, Color.WHITE.value)

        # Button's width and height will be the maximum size for the text
        maxTextW = recc.width
        maxTextH = recc.height

        # Reduce the maximum size so that the text is inside the button
        maxTextW *= size
        maxTextH *= size

        # Scale down the font size for width and height
        if text.get_width() > maxTextW or text.get_height() > maxTextH:
            # Calculate the difference in proportion between text and button
            scalingFactorW = maxTextW / text.get_width()
            scalingFactorH = maxTextH / text.get_height()

            # Choose the smaller of the two scaling factors
            scaling_factor = min(scalingFactorW, scalingFactorH)

            # Apply the scaling factor to the font size
            newFontSize = int(font.get_height() * scaling_factor)

            # Render the text with the updated font size
            font = py.font.Font(fontBox, newFontSize)
            text = font.render(textBox, True, Color.WHITE.value)
 
        return text

