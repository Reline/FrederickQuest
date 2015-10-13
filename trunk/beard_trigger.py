import pygame
import trigger

from trigger import *

class Beard_Trigger(Trigger):
	def __init__(self, x, y, image):
		Trigger.__init__(self, x, y, image, 'beard trigger')

	def give_beard(self, player):
		if self.activated == False:
			player.mustache_numb += 1
			self.activated = True