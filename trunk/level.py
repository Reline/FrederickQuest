import pygame
import entity
import constants
import player

from entity import *
from constants import *
from player import *

class Level():
	def __init__(self, mapGrid, player, triggers, entities, background_entities, collidables, camera, reset, barbers):
		self.mapGrid = mapGrid
		self.player = player
		self.triggers = triggers
		self.entities = entities
		self.background_entities = background_entities
		self.collidables = collidables
		self.camera = camera
		self.reset = reset
		self.barbers = barbers

	def resetLevel(self):
		self.player = Player(self.reset['player'].rect.left, self.reset['player'].rect.top)

		self.entities = pygame.sprite.Group()
		self.collidables = []
		self.barbers = []

		self.entities.add(self.player)
		
		for trigger in self.reset['triggers']:
			trigger.set(False)

		for collidable in self.reset['collidables']:
			self.entities.add(collidable)
			self.collidables.append(collidable)

		for barber in self.reset['barbers']:
			self.barbers.append(barber)
			self.entities.add(barber)

		self.background_entities = pygame.sprite.Group()
		for bg_entity in self.reset['background_entities'].sprites():
			self.background_entities.add(bg_entity)

	def completeLevel(self):
		self.resetLevel()