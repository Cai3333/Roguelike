#  __  __    _    ____ ___ ____ 
# |  \/  |  / \  / ___|_ _/ ___|
# | |\/| | / _ \| |  _ | | |    
# | |  | |/ ___ \ |_| || | |___ 
# |_|  |_/_/   \_\____|___\____|

import ai
import constants
import game
import globalvars
import maps
import menu

def cast_heal(caster, value):
    
    if caster.creature.current_hp == caster.creature.max_hp:
        game.message(caster.creature.name_instance + " the " + caster.name_object + " is already at full health!")
        return "canceled"
        
    else:
        game.message(caster.creature.name_instance + " the " + caster.name_object + " healed for " + str(value) + " health!")
        caster.creature.heal(value)
        
    return None

def cast_lighting(caster, T_damage_maxrange):
    
    damage, m_range= T_damage_maxrange
    
    player_location = (caster.x, caster.y)
    
    #  prompt the player for a tile
    point_selected = menu.tile_select(coords_origin = player_location, max_range = m_range, penetrate_walls = False)
    
    if point_selected:
        # convert that tile into a list of tiles between A -> B
        list_of_tiles = maps.find_line(player_location, point_selected)
    
        # cycle through list, damage everything found 
        for i, (x, y) in enumerate(list_of_tiles):
            target = maps.check_for_creature(x, y)
        
            if target:
                target.creature.take_damage(damage)

def cast_fireball_box(caster, T_damage_radius_range):
    
    # defs
    damage, local_radius, max_r = T_damage_radius_range
    
    caster_location = (caster.x, caster.y)
    
    # get target tile
    point_selected = menu.tile_select(coords_origin = caster_location, 
                                    max_range = max_r, penetrate_walls = False, 
                                    pierce_creature = False, radius_box = local_radius)
    
    if point_selected:
        # get sequence of tiles
        tiles_to_damage = maps.find_radius_box(point_selected, local_radius)
        
        creature_hit = False
        
        # damage all creatures in tiles
        for (x, y) in tiles_to_damage:
            creature_to_damage = maps.check_for_creature(x, y)
            
            if creature_to_damage:
                creature_to_damage.creature.take_damage(damage)

                if creature_to_damage is not globalvars.PLAYER:
                    creature_hit = True 
                    
        if creature_hit:
            game.message("The monster Howls out in pain.", constants.COLOR_RED)
            
def cast_fireball_diamond(caster, T_damage_radius_range):
    
    # defs
    damage, local_radius, max_r = T_damage_radius_range
    
    caster_location = (caster.x, caster.y)
    
    # get target tile
    point_selected = menu.tile_select(coords_origin = caster_location, 
                                    max_range = max_r, penetrate_walls = False, 
                                    pierce_creature = False, radius_diamond = local_radius)
    
    if point_selected:
        # get sequence of tiles
        tiles_to_damage = maps.find_radius_diamond(point_selected, local_radius)
        
        creature_hit = False
        
        # damage all creatures in tiles
        for (x, y) in tiles_to_damage:
            creature_to_damage = maps.check_for_creature(x, y)
            
            if creature_to_damage:
                creature_to_damage.creature.take_damage(damage)

                if creature_to_damage is not globalvars.PLAYER:
                    creature_hit = True 
                    
        if creature_hit:
            game.message("The monster Howls out in pain.", constants.COLOR_RED)  
                        
def cast_confusion(caster, effect_length):
    
    # Select tile
    point_selected = menu.tile_select()
    
    # Get target
    if point_selected:
        tile_x, tile_y = point_selected
        target = maps.check_for_creature(tile_x, tile_y)

        
        # Temporarily confuse the target
        if target:
            oldai = target.ai
            
            target.ai = ai.Confuse(old_ai = oldai, num_turns = effect_length)
            target.ai.owner = target
            
            game.message("The creature's eyes glaze over", constants.COLOR_GREEN) 
