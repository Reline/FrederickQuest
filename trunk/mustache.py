import pygame
import animation
import constants

from animation import *
from constants import *

MUSTACHES_MOVING = [IMAGES['stubble'], IMAGES['jumpstache'], IMAGES['invertstache_animation'], IMAGES['speedstache_animation'], IMAGES['godstache']]
MUSTACHES_IDLE = [IMAGES['stubble_idle'], IMAGES['jumpstache_idle'], IMAGES['invertstache_idle'], IMAGES['speedstache_idle'], IMAGES['godstache_idle']]

class Mustache(Animated_Entity):
	def __init__(self, x, y, idle_image, idle_fps, moving_image, moving_fps, type):
		Animated_Entity.__init__(self, idle_image, idle_fps, moving_image, moving_fps, type)

		self.current_idle_frame = 0
		self.current_moving_frame = 0

		self.image = self.idle_sprite_sheet[0]
		self.image.convert()
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)

	def update(self):
		if self.idle_sprite_sheet != None:
			self.current_idle_frame = get_animation_frame(pygame.time.get_ticks(), self.idle_fps, self.idle_frame_count)
		if self.moving_sprite_sheet != None:
			self.current_moving_frame = get_animation_frame(pygame.time.get_ticks(),self.moving_fps, self.moving_frame_count)