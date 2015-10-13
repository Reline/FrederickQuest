import pygame, sys, os, copy, random, math
import constants
import entity
import tile
import level
import player
import camera
import animation
import trigger
import beard_trigger
import barber

from pygame import *
from constants import *
from entity import *
from tile import *
from level import *
from player import *
from camera import *
from animation import *
from trigger import *
from beard_trigger import *
from barber import *

def main():
	pygame.init()
	pygame.mixer.init()
	pygame.mixer.music.set_volume(1.0)
	pygame.mixer.music.load('assets/Death_Waltz.wav')
	pygame.mixer.music.play(-1)

	levels = read_level_file("Level.txt")
	current_level = 0

	level = levels[current_level]

	while True:
		display_sequence_screens(SCREENS_INTRO)
		result = run_level(level)

		if result == 'quit':
			terminate()
		if result == 'dead':
			display_death_screen()
			level.resetLevel()
		if result == 'restart':
			level.restartLevel()
		# if result == 'completed':
		# 	display_sequence_screens(SCREENS_COMPLETED)

def display_screen(image):
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
			elif event.type == KEYDOWN:
				if event.key == K_RETURN:
					return 1

				return 1
		pygame.display.update()

def display_sequence_screens(screen_list):
	screen_number = 0

	while screen_number < len(screen_list):
		result = display_screen(screen_list[screen_number])
		screen_number += result

def display_life_lost_screen():
	index = random.randint(0, len(SCREENS_LIVES) - 1)
	display_screen(SCREENS_LIVES[index])

def display_death_screen():
	display_screen(SCREENS['screen_gameover'])

def run_level(level):
	player = level.player
	triggers = level.triggers
	entities = level.entities
	background_entities = level.background_entities
	camera = level.camera
	barbers = level.barbers

	while True:
		CLOCK.tick(FPS)

		key_presses = pygame.event.get(pygame.KEYDOWN)
		key_states = pygame.key.get_pressed()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return 'quit'

		if key_states[pygame.K_r]:
			return 'restart'

		if key_states[pygame.K_ESCAPE]:
			return 'quit'

		if player.life_lost == True:
			display_life_lost_screen()
			player.life_lost = False

		player.update(key_presses, key_states, level)
		player.mustache.update()
		camera.update(player)

		if player.dead == True:
			display_death_screen()
			return 'dead'

		if player.mustache_numb == 4 and player.completed == False:
			display_sequence_screens(SCREENS_COMPLETED)
			player.completed = True


		# draw the background
		for y in range(26):
			for x in range(20):
				SCREEN.blit(IMAGES['bg_wall'], (x * TILESIZE, y * TILESIZE))

		for entity in background_entities:
			entity.update()
			if entity.image.get_rect().colliderect(SCREEN.get_rect()):
				SCREEN.blit(entity.image, camera.apply(entity))

		for entity in triggers:
			SCREEN.blit(entity.image, camera.apply(entity))

		for barber in barbers:
			barber.update(level)

		for entity in entities:
			if entity.image.get_rect().colliderect(SCREEN.get_rect()):
				SCREEN.blit(entity.image, camera.apply(entity))
				SCREEN.blit(player.mustache.image, camera.apply(player))

		pygame.display.update()

def read_level_file(filename):
	assert os.path.exists(filename), 'Cannot find the level file: %s' % (filename)
	mapFile = open(filename, 'r')

	# Each level must end with a blank line
	content = mapFile.readlines() + ['\r\n']
	mapFile.close()

	levels = [] # Will contain a list of level objects.
	levelNum = 0
	mapBlueprintText = [] # contains the lines for a single level's map.
	mapGrid = [] # the map grid double array made from the data in mapBlueprintText.

	# Process each line in the level text to create the map grid
	for lineNum in range(len(content)):
		# Process each line that was in the level file.
		line = content[lineNum].rstrip('\r\n')

		if line != '':
			# This line is part of the map.
			mapBlueprintText.append(line)
		elif line == '' and len(mapBlueprintText) > 0:
			# A blank line indicates the end of a level's map in the file.
			# Convert the text in mapBlueprintText into a level object.

			# Find the longest row in the map.
			maxWidth = -1
			for i in range(len(mapBlueprintText)):
				if len(mapBlueprintText[i]) > maxWidth:
					maxWidth = len(mapBlueprintText[i])

			# Add spaces to the ends of the shorter rows. This
			# ensures the map will be rectangular.
			for i in range(len(mapBlueprintText)):
				mapBlueprintText[i] += ' ' * (maxWidth - len(mapBlueprintText[i]))

			# Convert mapBlueprintText to a map object.
			for x in range(len(mapBlueprintText[0])):
				mapGrid.append([])

			for y in range(len(mapBlueprintText)):
				for x in range(maxWidth):
				    mapGrid[x].append(mapBlueprintText[y][x])

			player = None
			playerX = None
			playerY = None

			camera = Camera(complex_camera, maxWidth*TILESIZE, LEVEL_HEIGHT)

			triggers = []
			collidables = []
			entities = pygame.sprite.Group()
			background_entities = pygame.sprite.Group()
			barbers = []

			# Loops through the levels file and creates objects that are in the level
			for x in range(maxWidth):
				for y in range(len(mapGrid[x])):

					# Entities

					if  mapGrid[x][y] in ('P'):
						# 'P' is player
						playerX = getPixelCoord(x)
						playerY = getPixelCoord(y)
						player = Player(getPixelCoord(x), getPixelCoord(y))
						entities.add(player)

					if mapGrid[x][y] in ('R'):
						# 'R' is Dwarf facing the right
						dwarf_idle = Animated_Tile(getPixelCoord(x), getPixelCoord(y), IMAGES['dwarf_idle'], 6, 32*SCALE, 'dwarf')
						background_entities.add(dwarf_idle)

					if mapGrid[x][y] in ('r'):
						# 'r' is Dwarf facing the left
						dwarf_idle = Animated_Tile(getPixelCoord(x), getPixelCoord(y), pygame.transform.flip(IMAGES['dwarf_idle'], True, False), 6, 32*SCALE, 'dwarf')
						background_entities.add(dwarf_idle)

					if mapGrid[x][y] in ('='):
						# 'r' is Dwarf facing the left
						dwarf_idle = Animated_Tile(getPixelCoord(x), getPixelCoord(y), pygame.transform.flip(IMAGES['dwarf_idle'], True, True), 6, 32*SCALE, 'dwarf')
						background_entities.add(dwarf_idle)

					if  mapGrid[x][y] in ('F'):
						# 'F' is a floor tile
						floor = Tile(getPixelCoord(x), getPixelCoord(y), IMAGES['floor'], 'floor')
						collidables.append(floor)
						entities.add(floor)

					if mapGrid[x][y] in ('W'):
						# 'W' is a wall tile
						wall = Tile(getPixelCoord(x), getPixelCoord(y), IMAGES['wall'], 'wall')
						collidables.append(wall)
						entities.add(wall)

					if mapGrid[x][y] in ('?'):
						# 'W' is a wall tile
						cabinet = Tile(getPixelCoord(x), getPixelCoord(y), IMAGES['cabinet'], 'cabinet')
						collidables.append(cabinet)
						entities.add(cabinet)

					if mapGrid[x][y] in ('+'):
						# 'W' is a wall tile
						cabinet = Tile(getPixelCoord(x), getPixelCoord(y), IMAGES['light'], 'death')
						collidables.append(cabinet)
						entities.add(cabinet)

					if mapGrid[x][y] in ('C'):
						# 'C' is a ceiling tile
						ceiling = Tile(getPixelCoord(x), getPixelCoord(y), IMAGES['ceiling'], 'ceiling')
						collidables.append(ceiling)
						entities.add(ceiling)

					if mapGrid[x][y] in ('E'):
						# 'E' is an enemy barber
						barberX = getPixelCoord(x)
						barberY = getPixelCoord(y)
						barber = Barber(barberX, barberY, 5, 5, True, False)
						#collidables.append(barber)
						entities.add(barber)
						barbers.append(barber)

					if mapGrid[x][y] in ('e'):
						# 'E' is an enemy barber
						barberX = getPixelCoord(x)
						barberY = getPixelCoord(y)
						barber = Barber(barberX, barberY, 5, 5, True, True)
						#collidables.append(barber)
						entities.add(barber)
						barbers.append(barber)

					# Background Entities
					if  mapGrid[x][y] in (''):
						# '' is a background wall tile
						bg_wall = Tile(getPixelCoord(x), getPixelCoord(y), IMAGES['bg_wall'], 'bg_wall')
						background_entities.append(bg_wall)

					if mapGrid[x][y] in ('L'):
						# 'L' is a light tile
						light = Tile(getPixelCoord(x), getPixelCoord(y), IMAGES['light'], 'light')
						background_entities.add(light)

					if mapGrid[x][y] in ('M'):
						# 'M' is a mirror tile
						mirror = Tile(getPixelCoord(x), getPixelCoord(y), IMAGES['mirror'], 'mirror')
						background_entities.add(mirror)

					if mapGrid[x][y] in ('m'):
						# 'M' is a mirror tile
						mirror = Tile(getPixelCoord(x), getPixelCoord(y), pygame.transform.flip(IMAGES['mirror'], False, True), 'mirror')
						background_entities.add(mirror)

					if mapGrid[x][y] in ('K'):
						# 'K' is a shelf tile
						shelf = Tile(getPixelCoord(x), getPixelCoord(y), IMAGES['shelf'], 'shelf')
						collidables.append(shelf)
						entities.add(shelf)

					if mapGrid[x][y] in ('k'):
						# 'k' is a mirror tile
						shelf = Tile(getPixelCoord(x), getPixelCoord(y), pygame.transform.flip(IMAGES['shelf'], False, True), 'shelf')
						collidables.append(shelf)
						entities.add(shelf)

					if mapGrid[x][y] in ('Z'):
						# 'Z' is a parlor pole tile
						parlor_pole = Animated_Tile(getPixelCoord(x), getPixelCoord(y), IMAGES['parlor_pole'], 2, 32*SCALE, 'parlor_pole')
						background_entities.add(parlor_pole)

					if mapGrid[x][y] in ('T'):
						# 'T' is a plant tile
						plant = Animated_Tile(getPixelCoord(x), getPixelCoord(y), IMAGES['plant'], 6, 32*SCALE, 'plant')
						background_entities.add(plant)

					if mapGrid[x][y] in ('1'):
						# '1' is door_1 tile
						door_1 = Tile(getPixelCoord(x), getPixelCoord(y), IMAGES['door_1'], 'door_1')
						background_entities.add(door_1)

					if mapGrid[x][y] in ('2'):
						# '2' is door_2 tile
						door_2 = Tile(getPixelCoord(x), getPixelCoord(y), IMAGES['door_2'], 'door_2')
						background_entities.add(door_2)

					if mapGrid[x][y] in ('3'):
						# '3' is door_3 tile
						door_3 = Tile(getPixelCoord(x), getPixelCoord(y), IMAGES['door_3'], 'door_3')
						background_entities.add(door_3)

					if mapGrid[x][y] in ('4'):
						# '3' is door_4 tile
						door_4 = Tile(getPixelCoord(x), getPixelCoord(y), IMAGES['door_4'], 'door_4')
						background_entities.add(door_4)

					if mapGrid[x][y] in ('N'):
						# 'N' is a window tile
						window = Tile(getPixelCoord(x), getPixelCoord(y), IMAGES['window'], 'window')
						background_entities.add(window)

					if mapGrid[x][y] in ('M'):
						# 'W' is a wall tile
						mirror = Tile(getPixelCoord(x), getPixelCoord(y), IMAGES['mirror'], 'mirror')
						background_entities.add(mirror)

					if mapGrid[x][y] in ('A'):
						# 'A' is a dwarven mirror/altar top half
						dwarven_mirror_top = Animated_Tile(getPixelCoord(x), getPixelCoord(y), IMAGES['dwarven_mirror_top'], 4, 32*SCALE, 'dwarven_mirror_top')
						background_entities.add(dwarven_mirror_top)

					if mapGrid[x][y] in ('B'):
						# 'B' is dwarven mirror/alter bottom half
						dwarven_mirror_bottom = Beard_Trigger(getPixelCoord(x), getPixelCoord(y), IMAGES['dwarven_mirror_bottom'])
						triggers.append(dwarven_mirror_bottom)

					if mapGrid[x][y] in ('a'):
						# 'a' is a dwarven mirror/altar top half
						dwarven_mirror_top = Animated_Tile(getPixelCoord(x), getPixelCoord(y), pygame.transform.flip(IMAGES['dwarven_mirror_top'], False, True), 4, 32*SCALE, 'dwarven_mirror_top')
						background_entities.add(dwarven_mirror_top)

					if mapGrid[x][y] in ('b'):
						# 'b' is dwarven mirror/alter bottom half
						dwarven_mirror_bottom = Beard_Trigger(getPixelCoord(x), getPixelCoord(y), pygame.transform.flip(IMAGES['dwarven_mirror_bottom'], False, True))
						triggers.append(dwarven_mirror_bottom)


			# Basic level design sanity checks:
			assert player != None, "Level %s (around line %s) in %s is missing a 'P' to mark the player's start point." % (levelNum+1, lineNum, filename)

			# Set of resettable variables to reset the level
			reset = {'player': copy.deepcopy(player),
				'triggers':copy.copy(triggers),
				'entities': copy.copy(entities),
				'barbers': copy.copy(barbers),
				'background_entities': copy.copy(background_entities),
				'collidables': copy.copy(collidables)}

			level = Level(mapGrid, player, triggers, entities, background_entities, collidables, camera, reset, barbers)

			#levels.append(levelObj)
			levels.append(level)

			# Reset the variables for reading the next map.
			mapBlueprintText = []
			mapGrid = []
			gameObjs = {}
			levelNum += 1
		
	return levels

def getPixelCoord(gridCoord):
	pixelCoord = gridCoord * TILESIZE
	return pixelCoord

def terminate():
	pygame.quit()
	sys.exit()

main()