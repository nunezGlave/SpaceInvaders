import pygame as py
from pygame import *
from Logical_Layer.Util.color import Color

class Button():
    # Parameterized Constructor
    def __init__(self, imageButton : Surface, scaleButton : float, textMessage : str, textFont : str, scaleText: float = 0.6, textColor: Color = Color.WHITE):
        # Get image's width and height
        width = imageButton.get_width()
        heigth = imageButton.get_height()

        # Scale image and initial position
        self.imageBtn = transform.scale(imageButton, (int(width * scaleButton), int(heigth * scaleButton)))
        self.rect = self.imageBtn.get_rect()

        # Create class attributes in relation to the text
        self.textFont = textFont
        self.textMessage = textMessage
        self.scaleText = 1 if scaleText > 1 else 0.1 if scaleText < 0.1 else scaleText
        self.textColor = textColor.value
        
        # Render text based on button size
        self.text = self._resizeText()
        self.txtRect = self.text.get_rect()

        # Event controller
        self.clicked = False

    # Draw a simple text button
    def draw(self, screen: Surface, btnPosX : int, btnPosY : int, textPerX : float = 0, textPerY : float = 0):
        # Set the initial position of the text in the center or change it according to the given position
        if textPerX == 0:
            textPosX = (self.rect.width - self.txtRect.width) // 2
        else:
            textPosX = self._btnPerW(textPerX)

        if textPerY == 0:
            textPosY = (self.rect.height - self.txtRect.height) // 2
        else:
            textPosY = self._btnPerH(textPerY)

        # Determine the new position of the text
        textPosX = btnPosX + textPosX
        textPosY = btnPosY + textPosY

        # Set new position for the button rectangle
        self.rect = self.imageBtn.get_rect(topleft = (btnPosX, btnPosY))

        # Set new position for the text rectangle
        self.txtRect = self.text.get_rect(topleft = (textPosX, textPosY))

        # Draw button on screen
        screen.blit(self.imageBtn, self.rect)

        # Draw the text on screen
        screen.blit(self.text, self.txtRect)

    # Draw a button containing an icon and text
    def drawIcon(self, screen: Surface, icon: Surface, btnPosX : int, btnPosY : int, elemPerX : int = 0, elemPerY : int = 0):
        # Scale icon size based on scaling factors
        iconFx, iconFy = 0.4, 1.2
        self.icon = transform.scale(icon, (icon.get_width() * iconFx, self.txtRect.height * iconFy))
        self.iconRect = self.icon.get_rect()

        # Set the initial position of the element on the both axis
        if elemPerX == 0:
            elemPerX = self._btnPerW(12)
        else:
            elemPerX = self._btnPerW(elemPerX)

        if elemPerY != 0:
            elemPerY = self._btnPerH(elemPerY)

        # Determine the greatest height between the icon, text, and button
        largerHeight = max(self.iconRect.height, self.txtRect.height, self.rect.height)

        # Calculate the vertical position to align image and text
        iconPosY = (largerHeight - self.iconRect.height) // 2
        textPosY = (largerHeight - self.txtRect.height) // 2

        # Determine the new coordinates of the icon and text
        iconPosX = btnPosX + elemPerX
        textPosX = iconPosX + self.iconRect.width + 5

        iconPosY = btnPosY + iconPosY + elemPerY
        textPosY = btnPosY + textPosY + elemPerY

        # Set new position for the button rectangle
        self.rect = self.imageBtn.get_rect(topleft = (btnPosX, btnPosY))

        # Set new position for the icon rectangle
        self.iconRect = self.icon.get_rect(topleft = (iconPosX, iconPosY)) 

        # Set new position for the text rectangle
        self.txtRect = self.text.get_rect(topleft = (textPosX, textPosY)) 

        # Draw button on screen
        screen.blit(self.imageBtn, self.rect)
        
        # Draw icon on screen
        screen.blit(self.icon, self.iconRect)   

        # Draw text on screen
        screen.blit(self.text, self.txtRect)

    # Flip image
    def flip(self, flipX: bool , flipY : bool):
        self.imageBtn = transform.flip(self.imageBtn, flipX, flipY)

    # Capture click event
    def mouseClick(self) -> bool:
        action = False
        # Get mouse position
        pos = mouse.get_pos()

        # Check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
            
        if mouse.get_pressed()[0] == 0:
            self.clicked = False

        return action
    
    # Resize font size
    def _resizeText(self) -> Surface:
        # Initial text rendering
        startFontSize = 1000
        font = py.font.Font(self.textFont, startFontSize)
        text : Surface = font.render(self.textMessage, True, self.textColor)

        # Button's width and height will be the maximum size for the text
        maxTextW = self.rect.width
        maxTextH = self.rect.height

        # Reduce the maximum size so that the text is inside the button
        maxTextW *= self.scaleText
        maxTextH *= self.scaleText

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
            font = py.font.Font(self.textFont, newFontSize)
            text = font.render(self.textMessage, True, self.textColor)

        return text

    # Calculate the percentage of the button width
    def _btnPerW(self, percentage: float):
        if (percentage >= 1 and percentage <= 100):
            screenPer = self.imageBtn.get_width() * (percentage / 100)
            return int(screenPer)
        else:
            raise Exception("The percentage must be between 0 and 100.")
    
    # Calculate the percentage of the button heigth
    def _btnPerH(self, percentage: float): 
        if (percentage >= 1 and percentage <= 100):
            screenPer = self.imageBtn.get_height() * (percentage / 100)
            return int(screenPer)
        else:
            raise Exception("The percentage must be between 0 and 100.")
    

