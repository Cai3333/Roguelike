# 3rd party modules
import pygame
import tcod as libtcod

# Game files
import constants

# Global constants
SURFACE_MAIN = None
GAME_MAP = None
PLAYER = None




#  ____  _                   _   
# / ___|| |_ _ __ _   _  ___| |_ 
# \___ \| __| '__| | | |/ __| __|
#  ___) | |_| |  | |_| | (__| |_ 
# |____/ \__|_|   \__,_|\___|\__|

class StrucTile:
    def __init__(self, block_path):
        self.block_path = block_path
        


#   ___  _     _           _       
#  / _ \| |__ (_) ___  ___| |_ ___ 
# | | | | '_ \| |/ _ \/ __| __/ __|
# | |_| | |_) | |  __/ (__| |_\__ \
#  \___/|_.__// |\___|\___|\__|___/
#           |__/    

class ObjActor:
    def __init__(self, x, y, sprite):
        self.x = x  # Map addres
        self.y = y  # Map addres
        self.sprite = sprite
        
    def draw(self):
        # draw the character
        SURFACE_MAIN.blit(self.sprite, ( self.x*constants.CELL_WIDTH, self.y*constants.CELL_HEIGHT))
        
    def move(self, dx, dy):
        # Move if current position plus new position is not wall
        if GAME_MAP[self.x + dx][self.y +dy].block_path == False:
            self.x += dx
            self.y += dy



#  __  __             
# |  \/  | __ _ _ __  
# | |\/| |/ _` | '_ \ 
# | |  | | (_| | |_) |
# |_|  |_|\__,_| .__/ 
#              |_| 

def map_create():
    new_map = [[StrucTile(False) for y in range(0, constants.MAP_HEIGHT)] for x in range(0, constants.MAP_WIDTH)]
    
    new_map[10][10].block_path = True
    new_map[10][15].block_path = True
    
    return new_map



#  ____                     _             
# |  _ \ _ __ __ ___      _(_)_ __   __ _ 
# | | | | '__/ _` \ \ /\ / / | '_ \ / _` |
# | |_| | | | (_| |\ V  V /| | | | | (_| |
# |____/|_|  \__,_| \_/\_/ |_|_| |_|\__, |
#                                   |___/ 

def draw_game():
    # clear the surface
    SURFACE_MAIN.fill(constants.COLOR_DEFAULT_BG)
    
    # draw the map
    draw_map(GAME_MAP)
    
    # draw the character
    PLAYER.draw()
    
    # Update the display
    pygame.display.flip()

def draw_map(map_to_draw):
    for x in range(0, constants.MAP_WIDTH):
        for y in range(0, constants.MAP_HEIGHT):
            if map_to_draw[x][y].block_path == True:
                # Draw wall
                SURFACE_MAIN.blit(constants.S_WALL, ( x*constants.CELL_WIDTH, y*constants.CELL_HEIGHT ))
            else:
                # Draw floor
                SURFACE_MAIN.blit(constants.S_FLOOR, ( x*constants.CELL_WIDTH, y*constants.CELL_HEIGHT ))





#   ____                      
#  / ___| __ _ _ __ ___   ___ 
# | |  _ / _` | '_ ` _ \ / _ \
# | |_| | (_| | | | | | |  __/
#  \____|\__,_|_| |_| |_|\___|

def game_main_loop():
    """"In this function, we loop the main game."""
    game_quit = False
    
    while not game_quit:
        # get player input
        events_list = pygame.event.get()
        
        # process input
        for event in events_list:  # loop through all events that have happened
            if event.type == pygame.QUIT:  # QUIT attribute - someone closed window
                game_quit = True
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    PLAYER.move(0, -1)
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    PLAYER.move(0, 1)
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    PLAYER.move(-1, 0)
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    PLAYER.move(1, 0)
                
        # TODO draw the game
        draw_game()
        
    # TODO quit the game
    pygame.quit()
    exit()


def game_initialize():
    """This function initializes the main window, in pygame."""
    
    global SURFACE_MAIN, GAME_MAP, PLAYER
    
    # initialize pygame
    pygame.init()
    
    SURFACE_MAIN = pygame.display.set_mode((constants.GAME_WIDTH, constants.GAME_HEIGHT))

    GAME_MAP = map_create()

    PLAYER = ObjActor(0, 0, constants.S_PLAYER)



#  __  __       _       
# |  \/  | __ _(_)_ __  
# | |\/| |/ _` | | '_ \ 
# | |  | | (_| | | | | |
# |_|  |_|\__,_|_|_| |_|

if __name__ == '__main__':
    game_initialize()
    game_main_loop()