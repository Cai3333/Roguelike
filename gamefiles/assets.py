import pygame
import startup
import constants
import globalvars

class ObjSpritesheet:
    '''Class used to grab images out of a sprite sheet.  As a class, it allows 
    you to access and subdivide portions of the sprite_sheet.
    Attributes:
        file_name (arg, str): String which contains the directory/filename of 
            the image for use as a spritesheet.
        sprite_sheet (pygame.surface): The loaded spritesheet accessed through 
            the file_name argument.
    '''
    
    def __init__(self, file_name):
        # Load the sprite sheet.
        self.sprite_sheet = pygame.image.load(file_name).convert()
        # {'a': 1, 'b': 2...}
        self.tiledict = {chr(i+96):i for i in range(1,27)}
        self.tiledict[0] = 0
        
    def get_image(self, column, row, width = constants.CELL_WIDTH, height = constants.CELL_HEIGHT,
                    scale = None):
        '''This method returns a single sprite.
        
        Args:
            column (str): Letter which gets converted into an integer, column in 
                the spritesheet to be loaded.
            row (int): row in the spritesheet to be loaded.
            width (int): individual sprite width in pixels
            height (int): individual sprite height in pixels
            scale ((width, height)) = If included, scales the sprites to a new 
                size.
        Returns:
            image_list (list): This method returns a single sprite contained 
                within a list loaded from the spritesheet property.
        '''
        
        image_list = []
                    
        image = pygame.Surface([width, height]).convert()
        
        image.blit(self.sprite_sheet, (0,0), (self.tiledict[column]*width, row*height, width, height))
        
        image.set_colorkey(constants.COLOR_BLACK)
            
        if scale:
            (new_w, new_h) = scale
            image = pygame.transform.scale(image, (new_w, new_h))
            
        image_list.append(image)
        
        return image_list

            
    def get_animation(self, column, row, width = constants.CELL_WIDTH, height = constants.CELL_HEIGHT,
                    num_sprites = 1, scale = None):
        '''This method returns a sequence of sprites.
        
        Args:
            column (str): Letter which gets converted into an integer, column in
                the spritesheet to be loaded.
            row (int): row in the spritesheet to be loaded.
            width (int): individual sprite width in pixels
            height (int): individual sprite height in pixels
            num_sprites (int): number of sprites to be loaded in sequence.
            scale ((width, height)) = If included, scales the sprites to a new 
                size.
        Returns:
            image_list (list): This method returns a sequence of sprites 
                contained within a list loaded from the spritesheet property.
        '''
        
        image_list = []
        
        for i in range(num_sprites):
            # Create blank image
            image = pygame.Surface([width, height]).convert()
            
            # copy image from sheet onto blank
            image.blit(self.sprite_sheet, (0,0), (self.tiledict[column]*width+(width*i), row*height, width, height))
            
            # set transparency key to black
            image.set_colorkey(constants.COLOR_BLACK)
            
            if scale:
                (new_w, new_h) = scale
                image = pygame.transform.scale(image, (new_w, new_h))
                
            image_list.append(image)
        
        return image_list  
    
class ObjAssets:
    '''This class is a struct that holds all the assets used in the
    game. This includes sprites, sound effects, and music.'''
    
    def __init__(self):
        # Complete sound list
        self.snd_list = []
        
        self.load_assets()
        self.volume_adjust()
        
    def load_assets(self):
        
        ###########
        ### ART ###
        ###########
        
        # SPRITESHEETS #
        self.reptile = ObjSpritesheet("data/graphics/Characters/Reptile.png")
        self.aquatic = ObjSpritesheet("data/graphics/Characters/Aquatic.png")
        self.rodent = ObjSpritesheet("data/graphics/Characters/Rodent.png")
        self.wall = ObjSpritesheet("data/graphics/Objects/Wall.png")
        self.floor = ObjSpritesheet("data/graphics/Objects/Floor.png")
        self.tile = ObjSpritesheet("data/graphics/Objects/Tile.png")
        
        self.shield = ObjSpritesheet("data/graphics/Items/Shield.png")
        self.medwep = ObjSpritesheet("data/graphics/Items/MedWep.png")
        self.shortwep = ObjSpritesheet("data/graphics/Items/ShortWep.png")
        self.longwep = ObjSpritesheet("data/graphics/Items/LongWep.png")
        self.armor = ObjSpritesheet("data/graphics/Items/Armor.png")
        self.scroll = ObjSpritesheet("data/graphics/Items/Scroll.png")
        self.flesh = ObjSpritesheet("data/graphics/Items/Flesh.png")
        self.misc = ObjSpritesheet("data/graphics/Items/Light.png")
        self.door0 = ObjSpritesheet("data/graphics/Objects/Door0.png")
        self.portal = ObjSpritesheet("data/graphics/Objects/portal.png")
        
        # ANIMATIONS #
        self.A_PLAYER = self.reptile.get_animation('o', 5, 16, 16, 2, (32, 32))
        self.A_SNAKE_01 = self.reptile.get_animation('e', 5, 16, 16, 2, (32, 32))
        self.A_SNAKE_02 = self.reptile.get_animation('k', 5, 16, 16, 2, (32, 32))
        self.A_MOUSE = self.rodent.get_animation(0, 0, 16, 16, 2, (32, 32))

        # SPRITES #
        self.S_WALL = self.wall.get_image('c', 6, 16, 16,(32, 32))[0]
        self.S_WALL_EXPLORED = self.wall.get_image('c', 12, 16, 16,(32, 32))[0]

        self.S_FLOOR = self.floor.get_image('a', 7, 16, 16,(32, 32))[0]
        self.S_FLOOR_EXPLORED = self.floor.get_image('a', 13, 16, 16,(32, 32))[0]
        
        # Items
        self.S_SWORD = self.medwep.get_image(0, 0, 16, 16,(32, 32))
        self.S_DAGGER = self.shortwep.get_image(0, 0, 16, 16,(32, 32))
        self.S_LONG_SWORD = self.longwep.get_image('c', 4, 16, 16,(32, 32))
        
        self.S_SHIELD = self.shield.get_image(0, 0, 16, 16,(32, 32))
        self.S_STRONG_SHIELD = self.shield.get_image('f', 0, 16, 16,(32, 32))
        
        self.S_ARMOR = self.armor.get_image(0, 0, 16, 16,(32, 32))
        self.S_STRONG_ARMOR = self.armor.get_image('f', 6, 16, 16,(32, 32))
        
        self.S_SCROLL_01 = self.scroll.get_image('d', 0, 16, 16,(32, 32))       
        self.S_SCROLL_02 = self.scroll.get_image('b', 1, 16, 16,(32, 32))
        self.S_SCROLL_03 = self.scroll.get_image('c', 5, 16, 16,(32, 32))    
        self.S_SCROLL_04 = self.scroll.get_image('c', 0, 16, 16,(32, 32))
        
        self.S_FLESH_01 = self.flesh.get_image('a', 3, 16, 16,(32, 32))
        self.S_FLESH_02 = self.flesh.get_image(0, 0, 16, 16,(32, 32))
        
        # SPECIAL
        self.S_STAIRS_DOWN = self.tile.get_image('e', 3, 16, 16, (32, 32))
        self.S_STAIRS_UP = self.tile.get_image('d', 3, 16, 16, (32, 32))
        self.MAIN_MENU_BG = pygame.image.load('data/graphics/snake_menu.jpg')
        self.MAIN_MENU_BG = pygame.transform.scale(self.MAIN_MENU_BG, (constants.CAMERA_WIDTH, constants.CAMERA_HEIGHT))
        
        self.S_MAGIC_LAMP = self.misc.get_image('d', 0, 16, 16, (32, 32))
        self.S_PORTALCLOSED = self.door0.get_image('f', 5, 16, 16, (32, 32))
        self.S_PORTALOPEN = self.portal.get_animation(0, 0, 16, 16, 2, (32, 32))
        
        self.animation_dict = {
            
            # ANIMATIONS #
            'A_globalvars.PLAYER' : self.A_PLAYER,
            'A_SNAKE_01' : self.A_SNAKE_01,
            'A_SNAKE_02' : self.A_SNAKE_02,
            'A_MOUSE' : self.A_MOUSE,  
            
            # Items
            'S_SWORD' : self.S_SWORD,
            'S_DAGGER' : self.S_DAGGER,
            'S_LONG_SWORD' : self.S_LONG_SWORD,
            
            'S_SHIELD' : self.S_SHIELD,
            'S_STRONG_SHIELD' : self.S_STRONG_SHIELD,
            
            'S_ARMOR' : self.S_ARMOR, 
            'S_STRONG_ARMOR' : self.S_STRONG_ARMOR, 
            
            'S_SCROLL_01' : self.S_SCROLL_01,     
            'S_SCROLL_02' : self.S_SCROLL_02,
            'S_SCROLL_03' : self.S_SCROLL_03,     
            'S_SCROLL_04' : self.S_SCROLL_04, 
            
            'S_FLESH_01' : self.S_FLESH_01,
            'S_FLESH_02' : self.S_FLESH_02,
            
            # SPECIAL
            'S_STAIRS_DOWN' : self.S_STAIRS_DOWN,
            'S_STAIRS_UP' : self.S_STAIRS_UP,
            'S_MAGIC_LAMP' : self.S_MAGIC_LAMP,
            'S_PORTALCLOSED' : self.S_PORTALCLOSED,
            "S_PORTALOPEN" : self.S_PORTALOPEN
            
        }

        ###########
        ## AUDIO ##
        ###########
        
        
        # loaded sound assets
        self.music_background = 'data/audio/music/forest-temple.mp3'
        self.music_menu = 'data/audio/music/Title Theme.mp3'
        self.snd_hit_1 = self.sound_add('data/audio/sound-effects/Hit_1.wav')
        self.snd_hit_2 = self.sound_add('data/audio/sound-effects/Hit_2.wav')
        self.snd_hit_3 = self.sound_add('data/audio/sound-effects/Hit_3.wav')
        self.snd_hit_4 = self.sound_add('data/audio/sound-effects/Hit_4.wav')
        
        # Sound list for player hitting creatures
        self.snd_list_hit = [self.snd_hit_1, self.snd_hit_2, self.snd_hit_3, self.snd_hit_4]
        
    def sound_add(self, file_address):
        
        new_sound = pygame.mixer.Sound(file_address)
        
        self.snd_list.append(new_sound)
        
        return new_sound
    
    def volume_adjust(self):
        for sound in self.snd_list:
            sound.set_volume(globalvars.PREFERENCES.vol_sound)
        
        pygame.mixer.music.set_volume(globalvars.PREFERENCES.vol_music)