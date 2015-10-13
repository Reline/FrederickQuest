import pygame
import constants
import entity
import animation

from constants import *
from entity import *
from animation import *

import math

class Barber(Animated_Entity):
	def __init__(self, x, y, speed, distance, right, upsidedown):
		Animated_Entity.__init__(self, None, None, IMAGES['barber_walk'], 5, 'Barber')
		self.speed = speed
		self.distance = distance*128
		self.initialX = x
		self.upsidedown = upsidedown
		if right == False:
			self.speed *=-1

		self.image = self.moving_sprite_sheet[0]
		self.image.convert()
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)

	def update(self, level):
		if self.moving_sprite_sheet != None:
			current_moving_frame = get_animation_frame(pygame.time.get_ticks(), self.moving_fps, self.moving_frame_count)

		if math.fabs(self.rect.left - self.initialX) > self.distance:
			self.speed*=-1

		if self.speed > 0:
			self.image = pygame.transform.flip(self.moving_sprite_sheet[current_moving_frame], False, self.upsidedown)
		else:
			self.image = pygame.transform.flip(self.moving_sprite_sheet[current_moving_frame], True, self.upsidedown)

		self.rect.left += self.speed

		self.collide(self.speed, 0, level)

	def collide(self, deltaX, deltaY, level):
		for entity in level.collidables:
			if pygame.sprite.collide_rect(self, entity):

				if deltaX > 0: 
					self.rect.right = entity.rect.left
					self.speed*=-1
				if deltaX < 0:
				 	self.rect.left = entity.rect.right
				 	self.speed*=-1