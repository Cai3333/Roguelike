#  __  __
# |  \/  | ___ _ __  _   _ ___
# | |\/| |/ _ \ '_ \| | | / __|
# | |  | |  __/ | | | |_| \__ \
# |_|  |_|\___|_| |_|\__,_|___/

# standard libraries
import sys

# libraries
import pygame

# game files
import constants
import draw
import game
import globalvars
import maps
import text
import tcod as libtcod


def main():
    
    menu_running = True
    
    # Start menu music
    pygame.mixer.music.load(globalvars.ASSETS.music_menu)
    pygame.mixer.music.play(-1)
    
    title_x = constants.CAMERA_WIDTH / 2 
    title_y = constants.CAMERA_HEIGHT / 2 - 40
    title_text = "Python - RL"
    
    # Button addreses
    continue_button_y = title_y + 40
    new_game_button_y = continue_button_y + 40
    options_button_y = new_game_button_y + 40
    quit_button_y = options_button_y + 40
    
    continue_game_button = draw.UiButton(globalvars.SURFACE_MAIN, 'CONTINUE', (150, 30), (title_x, continue_button_y))
    
    new_game_button = draw.UiButton(globalvars.SURFACE_MAIN, 'NEW GAME', (150, 30), (title_x, new_game_button_y))
    
    options_button = draw.UiButton(globalvars.SURFACE_MAIN, 'OPTIONS', (150, 30), (title_x, options_button_y))
    
    quit_button = draw.UiButton(globalvars.SURFACE_MAIN, 'QUIT', (150, 30), (title_x, quit_button_y))

    
    while menu_running:
        
        list_of_events = pygame.event.get()
        mouse_position = pygame.mouse.get_pos()
        
        game_input = (list_of_events, mouse_position)
        
        # Handle menu events
        for event in list_of_events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        # If continue
        if continue_game_button.update(game_input):
            
            # Stop music menu
            pygame.mixer.music.stop()
            
            # Start music game
            pygame.mixer.music.load(globalvars.ASSETS.music_background)
            pygame.mixer.music.play(-1)
            
            # try to load game, start new if problems.
            try:
                game.load()
            except:
                game.new()

            game.main_loop()
    
        # If new game
        if new_game_button.update(game_input):
            
            # Stop music menu
            pygame.mixer.music.stop()
            
            # Start music game
            pygame.mixer.music.load(globalvars.ASSETS.music_background)
            pygame.mixer.music.play(-1)
            
            game.new()
            game.main_loop()
        
        if options_button.update(game_input):
            options()
        
        if quit_button.update(game_input):
            pygame.quit()
            sys.exit()
        
        # draw menu
        globalvars.SURFACE_MAIN.blit(globalvars.ASSETS.MAIN_MENU_BG, (0, 0))
        
        text.display(globalvars.SURFACE_MAIN, title_text, constants.FONT_TITLE_SCREEN, (title_x, title_y - 20), 
                    constants.COLOR_RED, back_color = constants.COLOR_BLACK, center = True)
        
        # Draw the buttons
        continue_game_button.draw()
        new_game_button.draw()
        options_button.draw()
        quit_button.draw()
        
        # update surface
        pygame.display.update()
        
        globalvars.CLOCK.tick(constants.GAME_FPS)

def options():
    
    # Menu vars
    settings_menu_width = 200
    settings_menu_height = 200
    settings_menu_bgcolor = constants.COLOR_GREY
    
    # Slider vars
    slider_x = constants.CAMERA_WIDTH / 2
    sound_effect_slider_y = constants.CAMERA_HEIGHT / 2 - 60
    sound_effect_vol = .5
    music_effect_slider_y = sound_effect_slider_y + 50
    
    # Text vars
    text_y_offset = 20
    sound_text_y = sound_effect_slider_y - text_y_offset
    music_text_y = music_effect_slider_y - text_y_offset
    
    # Button vars
    button_save_y = music_effect_slider_y + 50
    
    window_center = (constants.CAMERA_WIDTH / 2, constants.CAMERA_HEIGHT / 2)

    settings_menu_surface = pygame.Surface((settings_menu_width, settings_menu_height))
    
    settings_menu_rect = pygame.Rect(0, 0, settings_menu_width, settings_menu_height)
    
    settings_menu_rect.center = window_center
    
    menu_close = False
    
    sound_effect_slider = draw.UiSlider(globalvars.SURFACE_MAIN, (125, 15),
                                (slider_x, sound_effect_slider_y),
                                constants.COLOR_RED,
                                constants.COLOR_GREEN,
                                globalvars.PREFERENCES.vol_sound)
    
    music_effect_slider = draw.UiSlider(globalvars.SURFACE_MAIN, (125, 15),
                                (slider_x, music_effect_slider_y),
                                constants.COLOR_RED,
                                constants.COLOR_GREEN,
                                globalvars.PREFERENCES.vol_music)
    
    save_button = draw.UiButton(globalvars.SURFACE_MAIN, 'SAVE', (60, 30), (slider_x, button_save_y), 
                        constants.COLOR_DARKERGREY, constants.COLOR_DGREY, constants.COLOR_BLACK, constants.COLOR_BLACK)
    
    while not menu_close:
        
        list_of_events = pygame.event.get()
        mouse_position = pygame.mouse.get_pos()
        
        game_input = (list_of_events, mouse_position)
        
        # Handle menu events
        for event in list_of_events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu_close = True

        current_sound_vol = globalvars.PREFERENCES.vol_sound
        current_music_vol = globalvars.PREFERENCES.vol_music
        
        sound_effect_slider.update(game_input)
        music_effect_slider.update(game_input)
        
        if current_sound_vol is not sound_effect_slider.current_val:
            globalvars.PREFERENCES.vol_sound = sound_effect_slider.current_val
            globalvars.ASSETS.volume_adjust()
        
        if current_music_vol is not music_effect_slider.current_val:
            globalvars.PREFERENCES.vol_music = music_effect_slider.current_val
            globalvars.ASSETS.volume_adjust()
            
        if save_button.update(game_input):
            game.preferences_save()
            menu_close = True
        
        # Draw the menu
        settings_menu_surface.fill(settings_menu_bgcolor)
        
        globalvars.SURFACE_MAIN.blit(settings_menu_surface, settings_menu_rect.topleft)
        
        text.display(globalvars.SURFACE_MAIN, "SOUND", 
                constants.FONT_DEBUG_MESSAGE, 
                (slider_x, sound_text_y),
                constants.COLOR_BLACK, center = True)
        
        text.display(globalvars.SURFACE_MAIN, "MUSIC", 
                constants.FONT_DEBUG_MESSAGE, 
                (slider_x, music_text_y),
                constants.COLOR_BLACK, center = True)
        
        sound_effect_slider.draw()
        music_effect_slider.draw()
        save_button.draw()
        
        pygame.display.update()

def pause():
    """This menu pauses the game and displays a simple message."""
    
    # Initiliaze to false, pause ends when set to True
    menu_close = False
    
    # window dimensions
    window_width = constants.CAMERA_WIDTH
    window_height = constants.CAMERA_HEIGHT
    
    # Window text characteristics
    menu_text = "PAUSED"
    menu_font = constants.FONT_DEBUG_MESSAGE
    
    # helper vars
    text_height =  text.get_height(menu_font)
    text_width = len(menu_text) * text.get_width(menu_font)
    
    while not menu_close: # While false, pause continues
        # get list of inputs
        events_list = pygame.event.get()
        
        # Evaluate each input
        for event in events_list:
            if event.type == pygame.QUIT:  # QUIT attribute - someone closed window
                game.closegame()
            
            # if key has been pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu_close = True
        
        # Draw pause message to screen        
        text.display(globalvars.SURFACE_MAIN, menu_text, menu_font, 
                ((window_width / 2) - (text_width / 2), (window_height / 2) - (text_height / 2)), constants.COLOR_WHITE, constants.COLOR_BLACK)

        globalvars.CLOCK.tick(constants.GAME_FPS)
        
        # Update the display surface
        pygame.display.flip()

def inventory():
    """Opens the inventory menu.
    
    The inventory allows the player to examine whatever items they are 
    curently holding. Selecting an item will drop it. 
    """
    
    # Initialize to false, when true, the menu will close
    menu_close = False
    
    # Calculate window dimensions
    window_width = constants.CAMERA_WIDTH
    window_height = constants.CAMERA_HEIGHT
    
    # Menu characteristics
    menu_width = 200
    menu_height = 200
    menu_x = (window_width / 2) - (menu_width / 2)
    menu_y = (window_height / 2) - (menu_height / 2)
    
    # Menu text characteristics
    menu_text_font = constants.FONT_INVENTORY
    menu_text_color = constants.COLOR_WHITE
    
    # Helper vars
    menu_text_height = text.get_height(menu_text_font)
    
    # Create surface to draw on.
    local_inv_surface = pygame.Surface((menu_width, menu_height))
    
    while not menu_close:
        # Clear the menu
        local_inv_surface.fill(constants.COLOR_BLACK)
        
        # Collect list of item names
        print_list = [obj.display_name for obj in globalvars.PLAYER.container.inventory]
        
        # List of input events
        events_list = pygame.event.get()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        mouse_x_rel = mouse_x - menu_x
        mouse_y_rel = mouse_y - menu_y
        
        mouse_in_window = (mouse_x_rel >= 0 and 
                            mouse_y_rel >= 0 and
                            mouse_x_rel <= menu_width and
                            mouse_y_rel <= menu_height)
        mouse_line_selection = int(mouse_y_rel / menu_text_height)
        
        # cycle through events
        for event in events_list:
            if event.type == pygame.QUIT:  # QUIT attribute - someone closed window
                game.closegame()
            
            # If press tab again, close menu
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    menu_close = True
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (event.button) == 1:
                    if (mouse_in_window and 
                    mouse_line_selection <= len(print_list) - 1):                        
                        obj = globalvars.PLAYER.container.inventory[mouse_line_selection].name_object
                        
                        globalvars.PLAYER.container.inventory[mouse_line_selection].item.use()
                        
                        if obj == "Lightning scroll" or obj == "Fireball-box scroll" or obj == "Fireball-diamond scroll" or obj == "Confusion scroll":
                            menu_close = True
                    
        # Draw the list
        for line, (name) in enumerate(print_list):
            
            if line == mouse_line_selection and mouse_in_window:
                text.display(local_inv_surface, name, menu_text_font, 
                        (0, 0 + (line * menu_text_height)), 
                        menu_text_color, constants.COLOR_GREY)
            else:
                text.display(local_inv_surface, name, menu_text_font, 
                        (0, 0 + (line * menu_text_height)), 
                        menu_text_color)
                
        # Render the game
        draw.game()      
        
        # Display menu
        globalvars.SURFACE_MAIN.blit(local_inv_surface, (menu_x, menu_y))
        
        globalvars.CLOCK.tick(constants.GAME_FPS)
        
        # Update display surface
        pygame.display.update()

def tile_select(coords_origin = None, max_range = None, radius_box = None, radius_diamond = None,
                        penetrate_walls = True, pierce_creature = True):
    ''' This menu let's the player select a tile
    
    This function pauses the game, produces an on screen rectangle and when the 
    player presses left mb, will return (message for now) the map address.
    '''

    menu_close = False
    
    while not menu_close:
        # Get mos position
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        # Get button click
        events_list = pygame.event.get()
        
        # mouse map selection
        
        mapx_pixel, mapy_pixel = globalvars.CAMERA.win_to_map((mouse_x, mouse_y))
        
        map_coord_x = int(mapx_pixel/constants.CELL_WIDTH)
        map_coord_y = int(mapy_pixel/constants.CELL_HEIGHT)
        
        valid_tiles = []
        
        if coords_origin:
            full_list_tiles = maps.find_line(coords_origin, (map_coord_x, map_coord_y))
            
            for i, (x,y) in enumerate(full_list_tiles):
                
                valid_tiles.append((x, y))
                
                # Stop at max range
                if max_range and i == max_range - 1:
                    break
                
                # Stop at wall    
                if not penetrate_walls and globalvars.GAME.current_map[x][y].block_path: 
                    break
                    
                # TODO stop at creature
                if not pierce_creature and maps.check_for_creature(x, y):
                    break
                    
        else:
            valid_tiles = [(map_coord_x, map_coord_y)]
                
        # return map_coords when presses left mb
        for event in events_list:
            if event.type == pygame.QUIT:  # QUIT attribute - someone closed window
                game.closegame()

            # If press tab again, close menu
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    menu_close = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # returns coordinate selected
                    return (valid_tiles[-1])
            
        # Draw game first
        globalvars.SURFACE_MAIN.fill(constants.COLOR_DEFAULT_BG)
        globalvars.SURFACE_MAP.fill(constants.COLOR_BLACK)
        
        globalvars.CAMERA.update()
        
        # draw the map
        draw.map_surface(globalvars.GAME.current_map)
        
        # draw all objects
        for obj in globalvars.GAME.current_objects:
            obj.draw()  
        
        # Draw rectangle at mouse position
        for (tile_x, tile_y) in valid_tiles:
            if (tile_x, tile_y) == valid_tiles[-1]:
                draw.tile_rect(coords = (tile_x, tile_y), mark = "X")
            else:
                draw.tile_rect(coords = (tile_x, tile_y))
        
        if radius_box:
            area_effect = maps.find_radius_box(valid_tiles[-1], radius_box)
            
            for (tile_x, tile_y) in area_effect:
                draw.tile_rect(coords = (tile_x, tile_y), 
                                tile_color = constants.COLOR_RED,
                                tile_alpha = 150)
                
        elif radius_diamond:
            area_effect = maps.find_radius_diamond(valid_tiles[-1], radius_diamond)
            
            for (tile_x, tile_y) in area_effect:
                draw.tile_rect(coords = (tile_x, tile_y), 
                                tile_color = constants.COLOR_RED,
                                tile_alpha = 150)
                
        globalvars.SURFACE_MAIN.blit(globalvars.SURFACE_MAP, (0, 0), globalvars.CAMERA.rectangle)
        
        draw.debug()
        draw.messages()
        
        # Update the display
        pygame.display.flip()
        
        # tick the CLOCK
        globalvars.CLOCK.tick(constants.GAME_FPS)

def level_up():
    
    # Menu vars
    settings_menu_width = 200
    settings_menu_height = 180
    settings_menu_bgcolor = constants.COLOR_GREY
    
    # Slider vars
    center_x = constants.CAMERA_WIDTH / 2
    # Button vars
    center_y = constants.CAMERA_HEIGHT / 2
    
    window_center = (center_x, center_y)

    settings_menu_surface = pygame.Surface((settings_menu_width, settings_menu_height))
    
    settings_menu_rect = pygame.Rect(0, 0, settings_menu_width, settings_menu_height)
    
    settings_menu_rect.center = window_center
    
    menu_close = False
    
    hp_button = draw.UiButton(globalvars.SURFACE_MAIN, "Max hp: " + str(globalvars.PLAYER.creature.max_hp), (145, 30), (center_x, center_y - 50), 
                        constants.COLOR_DARKERGREY, constants.COLOR_GREY, constants.COLOR_BLACK, constants.COLOR_BLACK)
    
    attack_button = draw.UiButton(globalvars.SURFACE_MAIN, "Attack: " + str(globalvars.PLAYER.creature.base_atk), (145, 30), (center_x, center_y), 
                        constants.COLOR_DARKERGREY, constants.COLOR_GREY, constants.COLOR_BLACK, constants.COLOR_BLACK)
    
    defense_button = draw.UiButton(globalvars.SURFACE_MAIN, "Defense: " + str(globalvars.PLAYER.creature.base_def), (145, 30), (center_x, center_y + 50), 
                        constants.COLOR_DARKERGREY, constants.COLOR_GREY, constants.COLOR_BLACK, constants.COLOR_BLACK)
    
    while not menu_close:
        
        list_of_events = pygame.event.get()
        mouse_position = pygame.mouse.get_pos()
        
        game_input = (list_of_events, mouse_position)
        
        # Handle menu events
        for event in list_of_events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
        if hp_button.update(game_input):
            globalvars.PLAYER.creature.max_hp += 5
            menu_close = True
            
        if attack_button.update(game_input):
            globalvars.PLAYER.creature.base_atk += 5
            menu_close = True
            
        if defense_button.update(game_input):
            globalvars.PLAYER.creature.base_def += 5
            menu_close = True
        
        # Draw the menu
        settings_menu_surface.fill(settings_menu_bgcolor)
        
        globalvars.SURFACE_MAIN.blit(settings_menu_surface, settings_menu_rect.topleft)
        
        hp_button.draw()
        attack_button.draw()
        defense_button.draw()
        
        globalvars.CLOCK.tick(constants.GAME_FPS)
        
        pygame.display.update()