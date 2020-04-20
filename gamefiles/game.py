
#   ____                      
#  / ___| __ _ _ __ ___   ___ 
# | |  _ / _` | '_ ` _ \ / _ \
# | |_| | (_| | | | | | |  __/
#  \____|\__,_|_| |_| |_|\___|

import gzip
import _pickle as pickle
import sys

import pygame

import actor
import constants
import draw
import generator
import globalvars
import maps
import menu


class ObjGame:
    '''The ObjGame tracks game progress
    This is an object that stores all the information used by the game to 'keep 
    track' of progress.  It tracks maps, objects, and game history or record of 
    messages.
    Attributes:
        current_map (obj): whatever map is currently loaded.
        current_objects (list): list of objects for the current map.
        message_history (list): list of messages that have been pushed
            to the player over the course of a game.'''
            
    def __init__(self):
        self.current_objects = []
        self.message_history = []
        self.map_previous = []
        self.map_next = []    
        self.current_map, self.current_rooms = maps.create()   
        
    def transition_next(self):
        
        globalvars.FOV_CALCULATE = True
                
        for obj in self.current_objects:
            obj.animation_destroy()
            
        self.map_previous.append((globalvars.PLAYER.x, globalvars.PLAYER.y, self.current_map, self.current_rooms, self.current_objects))    

        if len(self.map_next) == 0:
            
            self.current_objects = [globalvars.PLAYER]
            
            globalvars.PLAYER.animation_init()
            
            self.current_map, self.current_rooms = maps.create()   
            
            maps.place_objects(self.current_rooms)
        
        else:
            
            (globalvars.PLAYER.x, globalvars.PLAYER.y, self.current_map, self.current_rooms, self.current_objects) = self.map_next[-1]
            
            for obj in self.current_objects:
                obj.animation_init()
            
            maps.make_fov(self.current_map)
            
            globalvars.FOV_CALCULATE = True
            
            del self.map_next[-1]
        
    def transition_previous(self):
        
        if len(self.map_previous) != 0:

            for obj in self.current_objects:
                obj.animation_destroy()

            self.map_next.append((globalvars.PLAYER.x, globalvars.PLAYER.y, self.current_map, self.current_rooms, self.current_objects))
            
            (globalvars.PLAYER.x, globalvars.PLAYER.y, self.current_map, self.current_rooms, self.current_objects) = self.map_previous[-1]
            
            for obj in self.current_objects:
                obj.animation_init()
            
            maps.make_fov(self.current_map)
            
            globalvars.FOV_CALCULATE = True
            
            del self.map_previous[-1]   
            
def main_loop():
    """"In this function, we loop the main game."""
    game_quit = False
    
    # Player action definition
    player_action = "no-action"
    
    while not game_quit:
        # Handle player input
        player_action = handle_keys()
        
        maps.calculate_fov()
        
        if player_action == "Quit":
            closegame()
        
        for obj in globalvars.GAME.current_objects:
            if obj.ai:
                if player_action != "no-action":
                    obj.ai.take_turn()

            if obj.exitportal:
                obj.exitportal.update()
        
        if globalvars.PLAYER.state == "STATUS_DEAD" or globalvars.PLAYER.state == 'STATUS_WIN':
            game_quit = True
        
        # draw the game
        draw.game()
        
        # Update the display
        pygame.display.flip()
        
        # tick the CLOCK
        globalvars.CLOCK.tick(constants.GAME_FPS)
        
def handle_keys():
    '''Handles player input
    '''

    # get player input
    key_list = pygame.key.get_pressed()
    events_list = pygame.event.get()
    
    MOD_KEY = (key_list[pygame.K_LCTRL])
    
    # process input
    for event in events_list:  # loop through all events that have happened
        
        if event.type == pygame.QUIT:  #If close window, close
            return "Quit"
            
        if event.type == pygame.KEYDOWN:
            
            # Move up
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                globalvars.PLAYER.creature.move(0, -1)
                globalvars.FOV_CALCULATE = True
                return "player-moved"
            
            # Move down
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                globalvars.PLAYER.creature.move(0, 1)
                globalvars.FOV_CALCULATE = True
                return "player-moved"
            
            # Move left
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                globalvars.PLAYER.creature.move(-1, 0)
                globalvars.FOV_CALCULATE = True
                return "player-moved"
            
            # Move right
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                globalvars.PLAYER.creature.move(1, 0)
                globalvars.FOV_CALCULATE = True
                return "player-moved"
            
            # key 'e' -> pick up objects
            if event.key == pygame.K_e:
                objects_at_player = maps.objects_at_coords(globalvars.PLAYER.x, globalvars.PLAYER.y)
                
                for obj in objects_at_player:
                    if obj.item:
                        obj.item.pick_up(globalvars.PLAYER)
            
            if  event.key == pygame.K_f:
                list_of_objs = maps.objects_at_coords(globalvars.PLAYER.x, globalvars.PLAYER.y)
                
                for obj in list_of_objs:
                    if obj.stairs:
                        obj.stairs.use()
                    if obj.exitportal:
                        obj.exitportal.use()
            
            # key 'q' -> drop object from inventory
            if event.key == pygame.K_q:
                if len(globalvars.PLAYER.container.inventory) > 0:
                    globalvars.PLAYER.container.inventory[-1].item.drop(globalvars.PLAYER.x, globalvars.PLAYER.y)
            
            # key 'p' -> pause the game        
            if event.key == pygame.K_ESCAPE:
                menu.pause()
            
            # key 'TAB' ->  open inventory menu    
            if event.key == pygame.K_TAB:
                menu.inventory()
            
            
            
                    
    return "no-action"


def message(game_msg, msg_color = constants.COLOR_GREY):
    '''Adds message to the message history
    Args:
        game_msg (str): Message to be saved
        msg_color ((int, int, int), optional) = color of the message
    '''
    
    globalvars.GAME.message_history.append((game_msg, msg_color))



def new():
    # globalvars.GAME tracks game progress
    globalvars.GAME = ObjGame()

    generator.player((0, 0))

    maps.place_objects(globalvars.GAME.current_rooms)

def closegame():

    save()

    # quit the game
    pygame.quit()
    sys.exit()

def save():

    for obj in globalvars.GAME.current_objects:
        obj.animation_destroy()

    with gzip.open('data\savegame', 'wb') as file:
        pickle.dump([globalvars.GAME, globalvars.PLAYER], file)
        
        
def load():

    with gzip.open('data\savegame', 'rb') as file:
        globalvars.GAME, globalvars.PLAYER = pickle.load(file)

    for obj in globalvars.GAME.current_objects:
        obj.animation_init()

    # create FOV_MAP
    maps.make_fov(globalvars.GAME.current_map)

def preferences_save():
    with gzip.open('data\pref', 'wb') as file:
        pickle.dump(globalvars.PREFERENCES, file)

def preferences_load():

    with gzip.open('data\pref', 'rb') as file:
        globalvars.PREFERENCES = pickle.load(file)