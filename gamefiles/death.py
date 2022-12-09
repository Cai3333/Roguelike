#  ____             _   _     
# |  _ \  ___  __ _| |_| |__  
# | | | |/ _ \/ _` | __| '_ \ 
# | |_| |  __/ (_| | |_| | | |
# |____/ \___|\__,_|\__|_| |_|

import pygame

import constants
import game
import globalvars
import text

import datetime
import os


def snake(monster):
    """On death, monster stop moving."""
    
    # print message alerting player that creature has died
    game.message(f"{monster.creature.name_instance} is death!", constants.COLOR_GREY)

    # remove ai and creature components
    monster.animation = globalvars.ASSETS.S_FLESH_01
    monster.animation_key = "S_FLESH_01"
    monster.creature = None
    monster.ai = None

def mouse(mouse):
    # print message alerting player that creature has died
    game.message(f"{mouse.creature.name_instance} is death! Eat him for more health!", constants.COLOR_GREEN)

    # remove ai and creature components
    mouse.animation = globalvars.ASSETS.S_FLESH_02
    mouse.animation_key = "S_FLESH_02"
    mouse.creature = None
    mouse.ai = None
    
def player(player):
    player.state = "STATUS_DEAD"
    
    globalvars.SURFACE_MAIN.fill(constants.COLOR_BLACK)
    
    screen_center = (constants.CAMERA_WIDTH / 2, constants.CAMERA_HEIGHT / 2)

    text.display(globalvars.SURFACE_MAIN, "YOU DIED!", constants.FONT_TITLE_SCREEN, screen_center, constants.COLOR_WHITE, center = True)
    
    pygame.display.update()
    
    filename = "data/legacy/" + globalvars.PLAYER.creature.name_instance + '.' + datetime.date.today().strftime('%d%B%Y') + (".txt")
    
    file_exists = os.path.isfile(filename)
    save_exists = os.path.isfile('data/savegame')
    
    if file_exists: os.remove(filename)
    if save_exists: os.remove('data/savegame')
    
    legacy_file = open(filename, 'a+')
    
    legacy_file.write('*************THIS CHARACTER LOST**************' + '\n')
    
    for message, color in globalvars.GAME.message_history:
        legacy_file.write(message + "\n")
    legacy_file.write("\n*****************END_FILE*******************\n\n\n")

    pygame.time.wait(2000)