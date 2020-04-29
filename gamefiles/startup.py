# library imports
import random
import pygame
import tcod as libtcod

#game files
import constants
import globalvars
import data
import camera
import assets
import game


'''This function initializes the main window, and pygame.

'''


pygame.init()

pygame.key.set_repeat(200,75)

# Initialize Preferences
try:
    game.preferences_load()
except:
    globalvars.PREFERENCES = data.StrucPreferences()    

libtcod.namegen_parse('data/namegen/jice_celtic.cfg')

# SURFACE_MAIN is the display surface, a special surface that serves as the
# root console of the whole game.  Anything that appears in the game must be
# drawn to this console before it will appear.
globalvars.SURFACE_MAIN = pygame.display.set_mode((constants.CAMERA_WIDTH, constants.CAMERA_HEIGHT))

globalvars.SURFACE_MAP = pygame.Surface((constants.MAP_WIDTH * constants.CELL_WIDTH, 
                                constants.MAP_HEIGHT * constants.CELL_HEIGHT))


globalvars.CAMERA = camera.ObjCamera()

# ASSETS stores the games assets
globalvars.ASSETS = assets.ObjAssets()     

# The CLOCK tracks and limits cpu cycles
globalvars.CLOCK = pygame.time.Clock()

# Random number engine
globalvars.RANDOM_ENGINE = random.SystemRandom()

# when FOV_CALCULATE is true, FOV recalculates
globalvars.FOV_CALCULATE = True