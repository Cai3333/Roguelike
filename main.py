# 3rd party modules
import pygame
import tcod as libtcod
# Game files
import constants

# Global constants
SURFACE_MAIN = None
PLAYER = None
ENEMY = None
FOV_MAP = None
FOV_CALCULATE = None
CLOCK = None
GAME = None



#  ____  _                   _   
# / ___|| |_ _ __ _   _  ___| |_ 
# \___ \| __| '__| | | |/ __| __|
#  ___) | |_| |  | |_| | (__| |_ 
# |____/ \__|_|   \__,_|\___|\__|

class StrucTile:
    def __init__(self, block_path):
        self.block_path = block_path
        self.explored = False






#   ___  _     _           _       
#  / _ \| |__ (_) ___  ___| |_ ___ 
# | | | | '_ \| |/ _ \/ __| __/ __|
# | |_| | |_) | |  __/ (__| |_\__ \
#  \___/|_.__// |\___|\___|\__|___/
#           |__/    

class ObjActor:
    def __init__(self, x, y, name_object, sprite, creature = None, ai = None):
        self.x = x  # Map addres
        self.y = y  # Map addres
        self.sprite = sprite
        
        self.creature = creature
        if creature:
            creature.owner = self


        self.ai = ai
        
        if ai:
            ai.owner = self
        
    def draw(self):
        # Is visible only if is in fov
        is_visible = libtcod.map_is_in_fov(FOV_MAP, self.x, self.y)
        # draw the character if is visible
        if is_visible:
            SURFACE_MAIN.blit(self.sprite, ( self.x*constants.CELL_WIDTH, self.y*constants.CELL_HEIGHT))
        

class ObjGame:
    def __init__(self):
        self.current_map = map_create()
        self.current_objects = []
        
        self.message_history = []        
        
        
        

#   ____ ___  __  __ ____   ___  _   _ _____ _   _ _____ ____  
#  / ___/ _ \|  \/  |  _ \ / _ \| \ | | ____| \ | |_   _/ ___| 
# | |  | | | | |\/| | |_) | | | |  \| |  _| |  \| | | | \___ \ 
# | |__| |_| | |  | |  __/| |_| | |\  | |___| |\  | | |  ___) |
#  \____\___/|_|  |_|_|    \___/|_| \_|_____|_| \_| |_| |____/ 

class CompCreature:
    """ Creatures have health, can damage other objects by attacking them and can die."""
    def __init__(self, name_instance, hp = 10, death_function = None):
        
        self.name_instance = name_instance
        self.maxhp = hp
        self.hp = hp
        self.death_function = death_function
        
    
    def move(self, dx, dy):
        # Is a wall if block_path is true
        tile_is_wall = (GAME.current_map[self.owner.x + dx][self.owner.y +dy].block_path == True)
        
        target = map_check_for_creature(self.owner.x + dx, self.owner.y + dy, self.owner)
        
        if target:
            self.attack(target, 2)
        
        # Move if current position plus new position is not wall
        if not tile_is_wall and target is None:
            self.owner.x += dx
            self.owner.y += dy
    
    
    def attack(self, target, damage):
        game_message(f"{self.name_instance} attacks {target.creature.name_instance} for {str(damage)} damage!", constants.COLOR_WHITE)
        target.creature.take_damage(damage)
    
    def take_damage(self, damage):
        self.hp -= damage
        game_message(f"{self.name_instance}'s health is {str(self.hp)}/{str(self.maxhp)}.", constants.COLOR_RED)
        
        if self.hp <= 0:
            if self.death_function is not None:
                self.death_function(self.owner)
                
# TODO class CompItem:



# TODO class CompContainers:








#     _    ___ 
#    / \  |_ _|
#   / _ \  | | 
#  / ___ \ | | 
# /_/   \_\___|

class AiTest:
    """Once per turn, execute."""
    def take_turn(self):
        # Random direction
        self.owner.creature.move(libtcod.random_get_int(0,-1, 1), libtcod.random_get_int(0,-1, 1))
            

def death_monster(monster):
    """On death, monster stop moving."""
    game_message(f"{monster.creature.name_instance} is death!", constants.COLOR_GREY)

    monster.creature = None
    monster.ai = None
    


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
    
    for x in range(constants.MAP_WIDTH):
        new_map[x][0].block_path = True
        new_map[x][constants.MAP_HEIGHT -1].block_path = True
    
    for y in range(constants.MAP_HEIGHT):
        new_map[0][y].block_path = True
        new_map[constants.MAP_HEIGHT -1][y].block_path = True
    
    map_make_fov(new_map)
    
    return new_map



def map_check_for_creature(xPos, yPos, exclude_object = None):
    
    for obj in GAME.current_objects:
        if (obj is not exclude_object and 
            obj.x == xPos and 
            obj.y == yPos and 
            obj.creature):
                return obj
    return None

def map_make_fov(incoming_map):
    global FOV_MAP
    
    FOV_MAP = libtcod.map.Map(constants.MAP_WIDTH, constants.MAP_HEIGHT)
    
    for y in range(constants.MAP_HEIGHT):
        for x in range(constants.MAP_WIDTH):
            libtcod.map_set_properties(FOV_MAP, x, y,
                not incoming_map[x][y].block_path, not incoming_map[x][y].block_path)
    
def map_calculate_fov():
    global FOV_CALCULATE
    
    if FOV_CALCULATE:
        FOV_CALCULATE = False
        libtcod.map.Map.compute_fov(FOV_MAP, PLAYER.x, PLAYER.y, constants.TORCH_RADIUS, constants.FOV_LIGHT_WALLS,
            constants.FOV_ALGO)


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
    draw_map(GAME.current_map)
    
    # draw all objects
    for obj in GAME.current_objects:
        obj.draw()  
    
    draw_debug()
    draw_messages()
    
    
    # Update the display
    pygame.display.flip()

def draw_map(map_to_draw):
    for x in range(0, constants.MAP_WIDTH):
        for y in range(0, constants.MAP_HEIGHT):
            
            is_visible = libtcod.map_is_in_fov(FOV_MAP, x, y)
            
            if is_visible:
                
                map_to_draw[x][y].explored = True
                
                if map_to_draw[x][y].block_path == True:
                    # Draw wall
                    SURFACE_MAIN.blit(constants.S_WALL, ( x*constants.CELL_WIDTH, y*constants.CELL_HEIGHT ))
                else:
                    # Draw floor
                    SURFACE_MAIN.blit(constants.S_FLOOR, ( x*constants.CELL_WIDTH, y*constants.CELL_HEIGHT ))
                    
            elif map_to_draw[x][y].explored:
                
                    if map_to_draw[x][y].block_path == True:
                        # Draw wall
                        SURFACE_MAIN.blit(constants.S_WALL_EXPLORED, ( x*constants.CELL_WIDTH, y*constants.CELL_HEIGHT ))
                    else:
                        # Draw floor
                        SURFACE_MAIN.blit(constants.S_FLOOR_EXPLORED, ( x*constants.CELL_WIDTH, y*constants.CELL_HEIGHT ))
                    
                    

def draw_debug():
    
    draw_text(SURFACE_MAIN, "fps:" + str(int(CLOCK.get_fps())), (0,0), constants.COLOR_WHITE, constants.COLOR_BLACK)


def draw_messages():
    to_draw = GAME.message_history[-(constants.NUM_MESSAGES):]
    
    text_height = helper_text_height(constants.FONT_MESSAGE_TEXT)
    
    start_y = (constants.MAP_HEIGHT*constants.CELL_HEIGHT - (constants.NUM_MESSAGES * text_height)) - 5
    
    for i, (message, color) in enumerate(to_draw):
        draw_text(SURFACE_MAIN, message, (0, start_y + (i * text_height)), color, constants.COLOR_BLACK)



def draw_text(display_surface, text_to_display, T_coords, text_color, back_color = None):
    """"This function takes in some text, and displays it on the reference surface."""

    text_surf, text_rect = helper_text_objects(text_to_display, text_color, back_color)
    
    text_rect.topleft = T_coords
    
    display_surface.blit(text_surf, text_rect)
    
    
    
    
    

#  _   _      _                 
# | | | | ___| |_ __   ___ _ __ 
# | |_| |/ _ \ | '_ \ / _ \ '__|
# |  _  |  __/ | |_) |  __/ |   
# |_| |_|\___|_| .__/ \___|_|   
#              |_|              

def helper_text_objects(incoming_text, incoming_color, incoming_bg):
    """Render text and gives rect."""
    
    if incoming_bg:
        Text_surface = constants.FONT_DEBUG_MESSAGE.render(incoming_text, True, incoming_color, incoming_bg)
        
    else: 
        Text_surface = constants.FONT_DEBUG_MESSAGE.render(incoming_text, True, incoming_color)
        
    return Text_surface, Text_surface.get_rect()

def helper_text_height(font):
    
    font_object = font.render('a', True, (0, 0, 0))
    font_rect = font_object.get_rect()
    
    return font_rect.height





#   ____                      
#  / ___| __ _ _ __ ___   ___ 
# | |  _ / _` | '_ ` _ \ / _ \
# | |_| | (_| | | | | | |  __/
#  \____|\__,_|_| |_| |_|\___|

def game_main_loop():
    """"In this function, we loop the main game."""
    game_quit = False
    
    # Player action definition
    player_action = "no-action"
    
    while not game_quit:
        # Handle player input
        player_action = game_handle_keys()
        
        map_calculate_fov()
        
        if player_action == "Quit":
            game_quit = True
        
        elif player_action != "no-action":
            for obj in GAME.current_objects:
                if obj.ai:
                    obj.ai.take_turn()
            
            
        # draw the game
        draw_game()
        
        CLOCK.tick(constants.GAME_FPS)
        
    # quit the game
    pygame.quit()
    exit()
    


def game_initialize():
    """This function initializes the main window, in pygame."""
    
    global SURFACE_MAIN, GAME, CLOCK, FOV_CALCULATE, PLAYER, ENEMY
    
    # initialize pygame
    pygame.init()
    
    SURFACE_MAIN = pygame.display.set_mode((constants.MAP_WIDTH*constants.CELL_WIDTH, 
                                        constants.MAP_HEIGHT*constants.CELL_HEIGHT))
    
    GAME = ObjGame()
    
    CLOCK = pygame.time.Clock()
    
    FOV_CALCULATE = True

    creature_com1 = CompCreature("greg")
    PLAYER = ObjActor(1, 1, "python", constants.S_PLAYER, creature = creature_com1)
    
    creature_com2 = CompCreature("jackie", death_function = death_monster)
    ai_com = AiTest()
    ENEMY = ObjActor(15, 15, "crab", constants.S_ENEMY,
                    creature = creature_com2, ai= ai_com)

    GAME.current_objects = [PLAYER, ENEMY]


def game_handle_keys():
    global FOV_CALCULATE
    # get player input
    events_list = pygame.event.get()
    
    # process input
    for event in events_list:  # loop through all events that have happened
        if event.type == pygame.QUIT:  # QUIT attribute - someone closed window
            return "Quit"
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                PLAYER.creature.move(0, -1)
                FOV_CALCULATE = True
                return "player-moved"
            
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                PLAYER.creature.move(0, 1)
                FOV_CALCULATE = True
                return "player-moved"
            
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                PLAYER.creature.move(-1, 0)
                FOV_CALCULATE = True
                return "player-moved"
            
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                PLAYER.creature.move(1, 0)
                FOV_CALCULATE = True
                return "player-moved"
            
    return "no-action"
            


def game_message(game_msg, msg_color):
    
    GAME.message_history.append((game_msg, msg_color))





#  __  __       _       
# |  \/  | __ _(_)_ __  
# | |\/| |/ _` | | '_ \ 
# | |  | | (_| | | | | |
# |_|  |_|\__,_|_|_| |_|

if __name__ == '__main__':
    game_initialize()
    game_main_loop()