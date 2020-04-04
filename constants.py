import pygame
import tcod as libtcod

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

# Map vars
MAP_WIDTH = 20
MAP_HEIGHT = 20

# Color definitions
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GREY = (100, 100, 100)

# Game colors
COLOR_DEFAULT_BG = COLOR_GREY




#  ____             _ _            
# / ___| _ __  _ __(_) |_ ___  ___ 
# \___ \| '_ \| '__| | __/ _ \/ __|
#  ___) | |_) | |  | | ||  __/\__ \
# |____/| .__/|_|  |_|\__\___||___/
#       |_| 
# Sprites
S_PLAYER = pygame.image.load("data/python.png")
S_ENEMY = pygame.image.load("data/crab.png")


S_WALL = pygame.image.load("data/wall.jpg")
S_WALL_EXPLORED = pygame.image.load("data/wall.jpg")

S_FLOOR = pygame.image.load("data/floor.jpg")
S_FLOOR_EXPLORED = pygame.image.load("data/floor.jpg")

# Dark blue setting of sprite
S_WALL_EXPLORED.fill ((40,50,60), special_flags=pygame.BLEND_RGBA_MULT)
S_FLOOR_EXPLORED.fill ((40,50,60), special_flags=pygame.BLEND_RGBA_MULT)

# FOV SETTINGS
FOV_ALGO = libtcod.FOV_BASIC
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 10