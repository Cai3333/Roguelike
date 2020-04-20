#     _    ___ 
#    / \  |_ _|
#   / _ \  | | 
#  / ___ \ | | 
# /_/   \_\___|

import tcod as libtcod

import globalvars
import game
import constants



class Confuse:
    '''Objects with this ai aimlessly wonder around'''
    
    """Once per turn, execute."""
    
    def __init__(self, old_ai, num_turns):
        self.old_ai = old_ai
        self.num_turns = num_turns
        
    def take_turn(self):
        
        if self.num_turns > 0:
            # Random direction
            self.owner.creature.move(libtcod.random_get_int(0,-1, 1), 
                                    libtcod.random_get_int(0,-1, 1))
            self.num_turns -= 1
        
        else:
            self.owner.ai = self.old_ai
            game.message( self.owner.display_name + " has broken free!",
                constants.COLOR_RED)
            
class Chase:
    '''A basic monster ai which chases and tries to harm player'''
    
    def take_turn(self):
        monster = self.owner
        
        if libtcod.map_is_in_fov(globalvars.FOV_MAP, monster.x, monster.y):
            # move towards the player if far away
            if monster.distance_to(globalvars.PLAYER) >= 2:
                self.owner.move_towards(globalvars.PLAYER)
            
            # if close enough, attack player
            elif globalvars.PLAYER.creature.current_hp > 0:
                monster.creature.attack(globalvars.PLAYER)

class Flee:
    def take_turn(self):
        monster = self.owner
        
        if libtcod.map_is_in_fov(globalvars.FOV_MAP, monster.x, monster.y):

            self.owner.move_away(globalvars.PLAYER)