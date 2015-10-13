import pygame

#constants
FPS = 60
SCALE = 4
TILESIZE = 32 * SCALE
WIDTH = 1280
HEIGHT = 640


LEVEL_HEIGHT = 640

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()

def scale(image):
	rect = image.get_rect()
	_, _, width, height = rect 
	return pygame.transform.scale(image, (width*SCALE, height*SCALE))

IMAGES = {
	'barber': scale(pygame.image.load("assets/barber.png").convert_alpha()),
	'barber_walk' : scale(pygame.image.load("assets/barber_walk.png").convert_alpha()),
	'bg_wall': scale(pygame.image.load("assets/bg_wall.png").convert_alpha()),
	'ceiling': scale(pygame.image.load("assets/ceiling_tile.png").convert_alpha()),
	'cabinet': scale(pygame.image.load("assets/cabinet.png").convert_alpha()),
	'door_1': scale(pygame.image.load("assets/door_1.png").convert_alpha()),
	'door_2': scale(pygame.image.load("assets/door_2.png").convert_alpha()),
	'door_3': scale(pygame.image.load("assets/door_3.png").convert_alpha()),
	'door_4': scale(pygame.image.load("assets/door_4.png").convert_alpha()),
	'dwarven_mirror': scale(pygame.image.load("assets/dwarven_mirror.png").convert_alpha()),
	'dwarven_mirror_animation' : scale(pygame.image.load("assets/dwarven_mirror_anim.png").convert_alpha()),
	'floor': scale(pygame.image.load("assets/floor.png").convert_alpha()),
	'shelf': scale(pygame.image.load("assets/bookshelf.png").convert_alpha()),
	'godstache': scale(pygame.image.load("assets/godstache.png").convert_alpha()),
	'godstache_idle': scale(pygame.image.load("assets/godstache_idle.png").convert_alpha()),
	'invertstache_idle': scale(pygame.image.load("assets/invertstache_idle.png").convert_alpha()),
	'invertstache_animation' : scale(pygame.image.load("assets/invertstache_animation.png").convert_alpha()),
	'invertstache': scale(pygame.image.load("assets/invertstache.png").convert_alpha()),
	'jumpstache_idle': scale(pygame.image.load("assets/jumpstache_idle.png").convert_alpha()),
	'jumpstache': scale(pygame.image.load("assets/jumpstache.png").convert_alpha()),
	'light': scale(pygame.image.load("assets/Light.png").convert_alpha()),
	'mirror': scale(pygame.image.load("assets/mirror.png").convert_alpha()),
	'parlor_pole': scale(pygame.image.load("assets/parlor_pole_anim.png").convert_alpha()),
	'plant': scale(pygame.image.load("assets/plant_animation.png").convert_alpha()),
	'player': scale(pygame.image.load("assets/player.png").convert_alpha()),
	'player_idle': scale(pygame.image.load("assets/player_idle.png").convert_alpha()),
	'player_jump': scale(pygame.image.load("assets/player_jump.png").convert_alpha()),
	'player_walk': scale(pygame.image.load("assets/player_walk.png").convert_alpha()),
	'razor': scale(pygame.image.load("assets/razor.png").convert_alpha()),
	'razor_animation': scale(pygame.image.load("assets/razor_animation.png").convert_alpha()),
	'speedstache': scale(pygame.image.load("assets/speedstache.png").convert_alpha()),
	'speedstache_animation': scale(pygame.image.load("assets/speedstache_animation.png").convert_alpha()),
	'speedstache_idle' : scale(pygame.image.load("assets/speedstache_idle.png").convert_alpha()),
	'stubble' : scale(pygame.image.load("assets/stubble.png").convert_alpha()),
	'stubble_idle' : scale(pygame.image.load("assets/stubble_idle.png").convert_alpha()),
	'wall': scale(pygame.image.load("assets/wall.png").convert_alpha()),
	'window': scale(pygame.image.load("assets/window.png").convert_alpha()),
	'dwarven_mirror_bottom' : scale(pygame.image.load("assets/dwarven_mirrorB.png").convert_alpha()),
	'dwarven_mirror_top' : scale(pygame.image.load("assets/dwarven_mirrorT.png").convert_alpha()),
	'dwarf_idle' : scale(pygame.image.load('assets/dwarf_idle.png').convert_alpha())
}

SCREENS = {
	'screen_big_deal' : pygame.image.load("assets/screen_big_deal.png"),
	'screen_blame' : pygame.image.load("assets/screen_blame.png"),
	'screen_crab' : pygame.image.load("assets/screen_crab.png"),
	'screen_credits' : pygame.image.load("assets/screen_credits.png"),
	'screen_five_weeks' : pygame.image.load("assets/screen_five_weeks.png"),
	'screen_lol' : pygame.image.load("assets/screen_lol.png"),
	'screen_instructions' : pygame.image.load("assets/screen_instructions.png"),
	'screen_short_story' : pygame.image.load("assets/screen_short_story.png"),
	'screen_simply' : pygame.image.load("assets/screen_simply.png"),
	'screen_title': pygame.image.load("assets/screen_title.png"),
	'screen_gameover' : pygame.image.load("assets/screen_gameover.png"),
	'screen_awareness' : pygame.image.load("assets/screen_awareness.png"),
	'screen_godstache' : pygame.image.load("assets/screen_godstache.png"),
	'screen_enjoy' : pygame.image.load("assets/screen_enjoy.png"),
	'screen_jumpstache' : pygame.image.load("assets/screen_jumpstache.png"),
	'screen_invertstache' : pygame.image.load("assets/screen_invertstache.png"),
	'screen_speedstache' : pygame.image.load("assets/screen_speedstache.png")
}

SCREENS_LIVES = [
	SCREENS['screen_big_deal'], SCREENS['screen_blame'], SCREENS['screen_five_weeks'], SCREENS['screen_simply'], SCREENS['screen_lol']
]

SCREENS_INTRO = [
	SCREENS['screen_title'], SCREENS['screen_credits'], SCREENS['screen_instructions'], SCREENS['screen_short_story'] 
]

SCREENS_HELP = [
	None, SCREENS['screen_jumpstache'], SCREENS['screen_invertstache'], SCREENS['screen_speedstache']
]

SCREENS_COMPLETED = [
	SCREENS['screen_godstache'], SCREENS['screen_awareness'], SCREENS['screen_enjoy']
]