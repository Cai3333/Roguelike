#  ____  _                   _   
# / ___|| |_ _ __ _   _  ___| |_ 
# \___ \| __| '__| | | |/ __| __|
#  ___) | |_| |  | |_| | (__| |_ 
# |____/ \__|_|   \__,_|\___|\__|

class StrucTile:
    '''This class functions as a struct that tracks the data for each
    tile within a map.
    Attributes:
    block_path (arg, bool): TRUE if tile prevents actors from moving
    through it under normal circumstances.
    explored (bool): Initializes to FALSE, set to true if player
    has seen it before.'''
    
    def __init__(self, block_path):
        self.block_path = block_path
        self.explored = False

class StrucPreferences:
    def __init__(self):
        self.vol_sound = .5
        self.vol_music = .5