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

# Map vars
MAP_WIDTH = 30
MAP_HEIGHT = 30

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
S_WALL = pygame.image.load("data/wall.png")
S_FLOOR = pygame.image.load("data/floor.jpg")