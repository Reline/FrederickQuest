import pygame
import entity

from entity import *

class Tile(Entity):
	def __init__(self, x, y, tileImage, type):
		Entity.__init__(self, type)
		self.image = tileImage
		self.image.convert()
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)

	
	def update(self):
		pass