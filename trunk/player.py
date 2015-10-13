import pygame
import entity
import constants
import animation
import mustache
import beard_trigger
import barber

from barber import *
from entity import *
from constants import *
from animation import *
from mustache import *
from beard_trigger import *

class Player(Animated_Entity):
	def __init__(self, x, y):
		Animated_Entity.__init__(self, IMAGES['player_idle'], 5, IMAGES['player_walk'], 5, "player")
		self.altarcoordinatex = x
		self.altarcoordinatey = y
		self.lives = 3
		self.deltaX = 1
		self.deltaY = 0
		self.onGround = False
		self.mustache_numb = 0
		self.speed = 8
		self.mustache = Mustache(x, y, MUSTACHES_IDLE[self.mustache_numb], 5, MUSTACHES_MOVING[self.mustache_numb], 6, 'Mustache')

		self.life_lost = False
		self.dead = False
		self.completed = False

		self.image = self.idle_sprite_sheet[0]
		self.image.convert()
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)

	def update(self, key_presses, key_states, level):
		if self.idle_sprite_sheet != None:
			current_idle_frame = get_animation_frame(pygame.time.get_ticks(), self.idle_fps, self.idle_frame_count)
		if self.moving_sprite_sheet != None:
			current_moving_frame = get_animation_frame(pygame.time.get_ticks(), self.moving_fps, self.moving_frame_count)

		jumpstache = False
		invertstache = False
		speedstache = False
		godstache = False

		if self.mustache_numb == 1: jumpstache = True
		if self.mustache_numb == 2: invertstache = True
		if self.mustache_numb == 3: speedstache = True
		if self.mustache_numb == 4:
			godstache = True
			self.completed = True


		# If player has SPEED BEARD or GOD BEARD
		if speedstache or godstache:
			self.speed = 16
		else:
			self.speed = 8

		# If player presses UP
		if key_states[pygame.K_UP]:
			# If player has INVERT BEARD
			if not invertstache:
				if self.onGround:

					# If player has JUMP BEARD or GOD BEARD
					if jumpstache or godstache:
						self.deltaY -= 18
					else:
						self.deltaY -= 13

					self.onGround = False
			else:
				pass

		# If player presses DOWN
		if key_states[pygame.K_DOWN]:
			# If player has INVERT BEARD
			if not invertstache:
				pass
			else:
				if self.onGround:
					self.deltaY += 14
					self.onGround = False

		# If player moves LEFT
		if key_states[pygame.K_LEFT]:
			# If player has INVERT BEARD
			if not invertstache:
				self.deltaX = -self.speed
			else:
				self.deltaX = self.speed

			if self.deltaY == 0:
				if speedstache:
					self.image = pygame.transform.flip(self.idle_sprite_sheet[0], True, False)
				else:
					self.image = pygame.transform.flip(self.moving_sprite_sheet[current_moving_frame], not invertstache, invertstache)

				self.mustache.image = pygame.transform.flip(self.mustache.moving_sprite_sheet[self.mustache.current_moving_frame], not invertstache, invertstache)

			self.rect.left += self.deltaX
			self.collide(self.deltaX, 0, level)

		# If player moves RIGHT
		if key_states[pygame.K_RIGHT]:
			# If player has INVERT BEARD
			if not invertstache:
				self.deltaX = self.speed
			else:
				self.deltaX = -self.speed

			if self.deltaY == 0:
				if speedstache:
					self.image = self.idle_sprite_sheet[0]
				else:
					self.image = pygame.transform.flip(self.moving_sprite_sheet[current_moving_frame], invertstache, invertstache)

				self.mustache.image = pygame.transform.flip(self.mustache.moving_sprite_sheet[self.mustache.current_moving_frame], invertstache, invertstache)
			
			self.rect.left += self.deltaX
			self.collide(self.deltaX, 0, level)

		if not self.onGround:
			# If player has INVERT BEARD
			if not invertstache:
				self.deltaY += .6
			else:
				self.deltaY -= .6

			# If player has INVERT BEARD
			if not invertstache:
				if self.deltaY > 30:
					self.deltaY = 30
			else:
				if self.deltaY < -30:
					self.deltaY = -30

		# If NOT pressing LEFT or RIGHT / Used for idle
		if not (key_states[pygame.K_LEFT] or key_states[pygame.K_RIGHT]):
			if self.onGround:
				if self.deltaX > 0:
					self.image = pygame.transform.flip(self.idle_sprite_sheet[current_idle_frame], False, invertstache)
					self.mustache.image = pygame.transform.flip(self.mustache.idle_sprite_sheet[self.mustache.current_idle_frame], False, invertstache)
				else:
					self.image = pygame.transform.flip(self.idle_sprite_sheet[current_idle_frame], True, invertstache)
					self.mustache.image = pygame.transform.flip(self.mustache.idle_sprite_sheet[self.mustache.current_idle_frame], True, invertstache)

		# If FALLING or JUMPING
		if self.deltaY < -1.6 or self.deltaY > 1.6:
			if self.deltaX > 0:
				self.image = pygame.transform.flip(IMAGES['player_jump'], False, invertstache)
				self.mustache.image = pygame.transform.flip(self.mustache.moving_sprite_sheet[self.mustache.current_moving_frame], False, invertstache)
			else:
				self.image = pygame.transform.flip(IMAGES['player_jump'], True, invertstache)
				self.mustache.image = pygame.transform.flip(self.mustache.moving_sprite_sheet[self.mustache.current_moving_frame], True, invertstache)

		self.rect.top += self.deltaY
		self.onGround = False
		self.collide(0, self.deltaY, level)
	
	def collide(self, deltaX, deltaY, level):
		for entity in level.collidables:
			if pygame.sprite.collide_rect(self, entity):

				if entity.type == 'death':
					self.lose_life()

				invertstache = False
				if self.mustache_numb == 2: invertstache = True

				if deltaX > 0: self.rect.right = entity.rect.left
				if deltaX < 0: self.rect.left = entity.rect.right
				if deltaY > 0:
					if not invertstache:
						self.rect.bottom = entity.rect.top
						self.onGround = True
						self.deltaY = 0
					else:
						self.rect.bottom = entity.rect.top
						self.deltaY = 0
				if deltaY < 0:
					if not invertstache:
						self.rect.top = entity.rect.bottom
						self.deltaY = 0
					else:
						self.rect.top = entity.rect.bottom
						self.onGround = True
						self.deltaY = 0

		for trigger in level.triggers:
			if pygame.sprite.collide_rect(self, trigger):
				if trigger.type == 'beard trigger':
					if trigger.activated == False:
						trigger.give_beard(self)
						self.display_help_screens()
						self.mustache = Mustache(self.rect.left, self.rect.top, MUSTACHES_IDLE[self.mustache_numb], 5, MUSTACHES_MOVING[self.mustache_numb], 6, 'Mustache')
						self.altarcoordinatex = trigger.rect.left
						self.altarcoordinatey = trigger.rect.top

		for barber in level.barbers:
			if pygame.sprite.collide_rect(self, barber):
				if barber.type == 'Barber':
					self.lose_life()

	def lose_life(self):
		self.lives -= 1
		if self.lives == 0:
			self.dead = True
		else:
			self.life_lost = True
			self.rect.left = self.altarcoordinatex
			self.rect.top = self.altarcoordinatey

	def display_help_screens(self):
		if self.mustache_numb > 3:
			pass
		else:
			self.display_screen(SCREENS_HELP[self.mustache_numb])

	def display_screen(self, image):
		image_rect = image.get_rect()
		image_rect.topleft = (0, 0)

		# start with drawing a blank color to the entire window:
		SCREEN.fill((0, 0, 0))

		# Draw the title image to the window:
		SCREEN.blit(image, image_rect)

		while True: # Main loop for the start SCREEN.
			CLOCK.tick(FPS)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					terminate()
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_RETURN:
						return 1

			pygame.display.update()