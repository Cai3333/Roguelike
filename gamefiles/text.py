
#  _____         _
# |_   _|____  _| |_
#   | |/ _ \ \/ / __|
#   | |  __/>  <| |_
#   |_|\___/_/\_\\__|

def display(display_surface, text_to_display, font, coords, text_color, back_color = None, center = False):
    ''' Displays text on the desired surface. 
    Args:
        display_surface (pygame.Surface): the surface the text is to be
            displayed on.
            
        text_to_display (str): what is the text to be written
        
        font (pygame.font.Font): font object the text will be written using
        
        coords ((int, int)): where on the display_surface will the object be
            written, the text will be drawn from the upper left corner of the 
            text.
            
        text_color ((int, int, int)): (R, G, B) color code for the desired color
            of the text.
            
        back_color ((int, int, int), optional): (R, G, B) color code for the 
            background.  If not included, the background is transparent.
    '''

    # get both the surface and rectangle of the desired message
    text_surf, text_rect = objects(text_to_display, font, text_color, back_color)
    
    # adjust the location of the surface based on the coordinates
    if not center:
        text_rect.topleft = coords
    else:
        text_rect.center = coords
        
    # draw the text onto the display surface.
    display_surface.blit(text_surf, text_rect)


def objects(incoming_text, incoming_font, incoming_color, incoming_bg):
    '''Generates the text objects used for drawing text.
    This function is most often used in conjuction with the draw_text method.  
    It generates the text objects used by draw_text to actually display whatever
    string is called by the method.
    Args:
        incoming_text (str):
        incoming_font (pygame.font.Font):
        incoming_color ((int, int, int)):
        incoming_bg ((int, int, int), optional):
    Returns:
        Text_surface (pygame.Surface):
        Text_surface.get_rect() (pygame.Rect): 
    '''
    
    # if there is a background color, render with that.
    if incoming_bg:
        Text_surface = incoming_font.render(incoming_text, True, incoming_color, incoming_bg)
        
    else: # otherwise, render without a background.
        Text_surface = incoming_font.render(incoming_text, True, incoming_color)
        
    return Text_surface, Text_surface.get_rect()

def get_height(font):
    '''Measures the height in pixels of a specified font.
    This method is used when you need the height of a font object.  Most often
    this is useful when designing UI elements where the exact height of a font 
    needs to be known.
    Args:
        font (pygame.font.Font): the font whose height is desired.
    Returns:
        font_rect.height (int): the height, in pixels, of the font.
    '''
    
    # render the font out
    # font_object = font.render("b", True, (0, 0, 0))
    # font_rect = font_object.get_rect()
    # print(font_rect.height)
    
    return font.get_height()

def get_width(font):
    '''Measures the width in pixels of a specified font.
    This method is used when you need the width of a font object.  Most often
    this is useful when designing UI elements where the exact width of a font 
    needs to be known.
    Args:
        font (pygame.font.Font): the font whose width is desired.
    Returns:
        font_rect.width (int): the width, in pixels, of the font.
    '''
    
    # render the font out
    font_object = font.render('a', True, (0, 0, 0))
    font_rect = font_object.get_rect()
    
    return font_rect.width