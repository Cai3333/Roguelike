import tcod as libtcod
import pygame

pygame.init()

#  ____                           
# / ___|  ___ _ __ ___  ___ _ __  
# \___ \ / __| '__/ _ \/ _ \ '_ \ 
#  ___) | (__| | |  __/  __/ | | |
# |____/ \___|_|  \___|\___|_| |_|

# Game sizes
GAME_WIDTH = 800
GAME_HEIGHT = 600
CELL_WIDTH = 32
CELL_HEIGHT =32

# FPS LIMIT
GAME_FPS = 63


# Map vars
MAP_WIDTH = 20
MAP_HEIGHT = 20

# Color definitions
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GREY = (100, 100, 100)
COLOR_RED = (255, 0, 0)

# Game colors
COLOR_DEFAULT_BG = COLOR_GREY

# FOV SETTINGS
FOV_ALGO = libtcod.FOV_BASIC  # Algorithm for FOV Calculation
FOV_LIGHT_WALLS = True        # Does the FOV shine on the walls?
TORCH_RADIUS = 10             # Sight radius for FOV

# MESSAGE DEFAULT
NUM_MESSAGES = 4

# FONTS #
FONT_DEBUG_MESSAGE = pygame.font.Font("data/joystix.ttf", 16)
FONT_MESSAGE_TEXT = pygame.font.Font("data/terminus.ttf", 14)