import pygame
from pygame import *

class Button():
	def __init__(self, image : Surface,  xPos: int, yPos: int, scale: float):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect(topleft = (xPos, yPos))
		self.clicked = False
		self.x = self.rect.x
		self.y = self.rect.y

	def draw(self, surface: Surface):
		action = False
		# Get mouse position
		pos = pygame.mouse.get_pos()

		# Check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		# Draw on screen
		surface.blit(self.image, (self.rect.x, self.rect.y))

		return action

	def xP(self, percentage: int):
		return self.image.get_width() * (percentage / 100)
	
	def yP(self, percentage: int):
		return self.image.get_height() * (percentage / 100)
