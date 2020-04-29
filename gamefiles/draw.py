#  ____                                  
# |  _ \ _ __ __ ___      _
# | | | | '__/ _` \ \ /\ / / 
# | |_| | | | (_| |\ V  V /  
# |____/|_|  \__,_| \_/\_/ 
#                                   

import pygame
import tcod as libtcod

import constants
import globalvars
import text
import actor

class UiButton:
    def __init__(self, surface, button_text, size, center_coords, 
                color_box_mouseover = constants.COLOR_RED, 
                color_box_default = constants.COLOR_GREEN, 
                color_text_mouseover = constants.COLOR_GREY, 
                color_text_default = constants.COLOR_GREY):

        self.surface = surface
        self.button_text = button_text
        self.size = size
        self.center_coords = center_coords
        
        self.c_box_mo = color_box_mouseover
        self.c_box_default = color_box_default
        self.c_text_mo = color_text_mouseover
        self.c_text_default = color_text_default
        self.c_c_box = color_box_default
        self.c_c_text = color_text_default
        
        self.rect = pygame.Rect((0, 0), size)
        self.rect.center = center_coords
        
    
    def update(self, player_input):
        mouse_clicked = False
        local_events, local_mousepos = player_input
        mouse_x, mouse_y = local_mousepos
        
        mouse_over = (mouse_x >= self.rect.left
                    and mouse_x <= self.rect.right
                    and mouse_y >= self.rect.top
                    and mouse_y <= self.rect.bottom)
        
        for event in local_events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_clicked = True
                    
        if mouse_over and mouse_clicked:
            return True
        
        if mouse_over:
            self.c_c_box = self.c_box_mo
            self.c_c_text = self.c_text_mo
            
        else: 
            self.c_c_box = self.c_box_default
            self.c_c_text = self.c_text_default
        
    def draw(self):
        pygame.draw.rect(self.surface, self.c_c_box, self.rect)
        text.display(self.surface, self.button_text, constants.FONT_DEBUG_MESSAGE, self.center_coords, self.c_c_text, center = True)
        
class UiSlider:
    def __init__(self, surface, size, center_coords, bg_color, fg_color, parameter_value):

        self.surface = surface
        self.size = size
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.current_val = parameter_value

        self.bg_rect = pygame.Rect((0, 0), size)
        self.bg_rect.center = center_coords
        self.fg_rect = pygame.Rect((0, 0), (self.bg_rect.w * self.current_val, self.bg_rect.h))
        self.fg_rect.topleft = self.bg_rect.topleft
        
        self.grip_tab = pygame.Rect((0, 0), (20, self.bg_rect.height + 4))
        self.grip_tab.center = (self.fg_rect.right, self.bg_rect.centery)
        
    def update(self, player_input):
        mouse_down = pygame.mouse.get_pressed()[0]
        
        local_events, local_mousepos = player_input
        mouse_x, mouse_y = local_mousepos
                
        mouse_over = (mouse_x >= self.bg_rect.left
                    and mouse_x <= self.bg_rect.right
                    and mouse_y >= self.bg_rect.top
                    and mouse_y <= self.bg_rect.bottom)
        
        if mouse_down and mouse_over:
            self.current_val = (mouse_x - self.bg_rect.left) / self.bg_rect.width
        
            self.fg_rect.width = self.bg_rect.width * self.current_val
            
            self.grip_tab.center = (self.fg_rect.right, self.bg_rect.centery)
        
    def draw(self):
        
        # Draw background rect
        pygame.draw.rect(self.surface, self.bg_color, self.bg_rect)
        
        # Draw foreground rect
        pygame.draw.rect(self.surface, self.fg_color, self.fg_rect)

        # Draw slider tab
        pygame.draw.rect(self.surface, constants.COLOR_BLACK, self.grip_tab)
        
def game():
    '''Main call for drawing the entirity of the game.
    This method is responsible for regularly drawing the whole game.  It starts
    by clearing the main surface, then draws elements of the screen from front
    to back.
    The order of operations is:
    1) Clear the screen
    2) Draw the map
    3) Draw the objects
    4) Draw the debug console
    5) Draw the messages console
    6) Update the display
    '''
    
    # clear the surface
    globalvars.SURFACE_MAIN.fill(constants.COLOR_DEFAULT_BG)
    globalvars.SURFACE_MAP.fill(constants.COLOR_BLACK)
    
    globalvars.CAMERA.update()
    
    # draw the map
    map_surface(globalvars.GAME.current_map)
    
    # draw all objects
    for obj in globalvars.GAME.current_objects:
        obj.draw()  

        if obj.name_object == 'python':
            obj.creature.draw_health()

        
    globalvars.SURFACE_MAIN.blit(globalvars.SURFACE_MAP, (0, 0), globalvars.CAMERA.rectangle)
    
    
    debug()
    messages()
    
def map_surface(map_to_draw):
    '''Main call for drawing a map to the screen.
    draw_map loops through every tile within the map and draws it's 
    corresponding tile to the screen.
    Args:
        map_to_draw (array): the map to draw in the background.  Under most
            circumstances, should be the GAME.current_map object.
    '''
        
    cam_x, cam_y = globalvars.CAMERA.map_address
    display_map_w = constants.CAMERA_WIDTH // constants.CELL_WIDTH
    display_map_h = constants.CAMERA_HEIGHT // constants.CELL_HEIGHT
    
    render_w_min = cam_x - (display_map_w // 2)
    render_h_min = cam_y - (display_map_h // 2)
    render_w_max = cam_x + (display_map_w // 2)
    render_h_max = cam_y + (display_map_h // 2)
    
    if render_w_min < 0: 
        render_w_min = 0
    if render_h_min < 0: 
        render_h_min = 0
    
    if render_w_max > constants.MAP_WIDTH: 
        render_w_max = constants.MAP_WIDTH
    if render_h_max > constants.MAP_HEIGHT: 
        render_h_max = constants.MAP_HEIGHT
    
    # Loop through every object in the map
    for x in range(render_w_min, render_w_max):
        for y in range(render_h_min, render_h_max):
            
            # Does this tile appear within the current FOV?
            is_visible = libtcod.map_is_in_fov(globalvars.FOV_MAP, x, y)
            
            if is_visible:
                
                # once the tile appears within the FOV, set to explored
                map_to_draw[x][y].explored = True
                
                # if tile is blocked, draw a wall.
                if map_to_draw[x][y].block_path == True:
                    # Draw wall
                    globalvars.SURFACE_MAP.blit(globalvars.ASSETS.S_WALL, ( x*constants.CELL_WIDTH, y*constants.CELL_HEIGHT ))
                else:
                    # Draw floor
                    globalvars.SURFACE_MAP.blit(globalvars.ASSETS.S_FLOOR, ( x*constants.CELL_WIDTH, y*constants.CELL_HEIGHT ))
            
            # if tile is not visible, is it explored?        
            elif map_to_draw[x][y].explored:
                
                    # if yes, and the tile is blocked, draw an explored wall.
                    if map_to_draw[x][y].block_path == True:
                        # Draw wall
                        globalvars.SURFACE_MAP.blit(globalvars.ASSETS.S_WALL_EXPLORED, ( x*constants.CELL_WIDTH, y*constants.CELL_HEIGHT ))
                    else:
                        # Draw floor
                        globalvars.SURFACE_MAP.blit(globalvars.ASSETS.S_FLOOR_EXPLORED, ( x*constants.CELL_WIDTH, y*constants.CELL_HEIGHT ))
                        
def debug():
    '''Draw the debug console to the display surface.
    This method draws a debug console to the upper left corner of the window.
    For now, this debug console is limited to the current FPS.
    '''    
    
    text.display(globalvars.SURFACE_MAIN, "fps:" + str(int(globalvars.CLOCK.get_fps())), constants.FONT_DEBUG_MESSAGE, (constants.CAMERA_WIDTH - 78,0), constants.COLOR_WHITE, constants.COLOR_BLACK)
    
def messages():
    '''Draw the messages console to the display surface.
    This method generates a list of messages to display in the lower left-hand
    corner of the display surface, and then displays them.
    '''

    # if the number of messages available is < than the number of messages we
    # are allowed to display, just display all messages
    to_draw = globalvars.GAME.message_history[-(constants.NUM_MESSAGES):]
    
    text_height = text.get_height(constants.FONT_MESSAGE_TEXT)
    
    start_y = (constants.CAMERA_HEIGHT - (constants.NUM_MESSAGES * text_height)) - 0
    
    for i, (message, color) in enumerate(to_draw):
        text.display(globalvars.SURFACE_MAIN, message, constants.FONT_MESSAGE_TEXT, 
                  (0, start_y + (i * text_height)), color, constants.COLOR_BLACK)
        
def tile_rect(coords, tile_color = None, tile_alpha = None, mark = None):
    
    x, y = coords
    
    # Default color
    if tile_color:
        local_color = tile_color
    else:
        local_color = constants.COLOR_WHITE
    
    # Default alpha
    if tile_alpha:
        local_alpha = tile_alpha
    else:
        local_alpha = 200
        
    new_x = x * constants.CELL_WIDTH
    new_y = y * constants.CELL_WIDTH
    
    new_surface = pygame.Surface((constants.CELL_WIDTH, constants.CELL_HEIGHT))
    
    new_surface.fill(local_color)
    
    new_surface.set_alpha(local_alpha)
    
    if mark:
        text.display(new_surface, mark, font = constants.FONT_CURSOR_TEXT,
                    coords = (constants.CELL_WIDTH /2, constants.CELL_HEIGHT / 2),
                    text_color = constants.COLOR_BLACK, center = True)
    
    globalvars.SURFACE_MAP.blit(new_surface, (new_x, new_y))
