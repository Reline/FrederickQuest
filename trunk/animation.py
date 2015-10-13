import pygame

import entity
import constants

from entity import *
from constants import *

class Animated_Entity(Entity):
	def __init__(self, idle_image, idle_fps, moving_image, moving_fps, type):
		Entity.__init__(self, type)

		if idle_image != None:
			self.idle_sprite_sheet = get_sprite_sheet((TILESIZE, TILESIZE), idle_image, TILESIZE)
			self.idle_frame_count = len(self.idle_sprite_sheet)
		else:
			self.idle_sprite_sheet = None

		if moving_image != None:
			self.moving_sprite_sheet = get_sprite_sheet((TILESIZE, TILESIZE), moving_image, TILESIZE)
			self.moving_frame_count = len(self.moving_sprite_sheet)		
		else:
			self.moving_sprite_sheet = None

		self.idle_fps = idle_fps
		self.moving_fps = moving_fps

class Animated_Tile(Entity):
	def __init__(self, x, y, idle_image, idle_fps, image_height, type):
		Entity.__init__(self, type)
		self.idle_sprite_sheet = get_sprite_sheet((TILESIZE, TILESIZE), idle_image, image_height)
		self.idle_frame_count = len(self.idle_sprite_sheet)
		self.idle_fps = idle_fps

		self.image = self.idle_sprite_sheet[0]
		self.image.convert()
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)

	def update(self):
		current_idle_frame = get_animation_frame(pygame.time.get_ticks(), self.idle_fps, self.idle_frame_count)
		self.image = self.idle_sprite_sheet[current_idle_frame]

def get_sprite_sheet(size,image, image_height, pos=(0,0)):

	#Initial Values
	len_sprt_x,len_sprt_y = size #sprite size
	sprt_rect_x,sprt_rect_y = pos #where to find first sprite on sheet

	sheet = image.convert_alpha() #Load the sheet
	sheet_rect = sheet.get_rect()
	sprites = []

	for i in range(0,sheet_rect.height,image_height):#rows
		sheet.set_clip(pygame.Rect(sprt_rect_x, sprt_rect_y, len_sprt_x, len_sprt_y)) #find sprite you want
		sprite = sheet.subsurface(sheet.get_clip()) #grab the sprite you want
		sprites.append(sprite)
		sprt_rect_y += len_sprt_y
		sprt_rect_x = 0

	return sprites

def get_animation_frame(millis, frames_per_second, framecount, start_millis=0):
    millis_per_frame = 1000 // frames_per_second
    elapsed_millis = millis - start_millis
    total_frames = elapsed_millis // millis_per_frame
    return total_frames % framecount