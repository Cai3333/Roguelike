
#   ____                           _
#  / ___| ___ _ __   ___ _ __ __ _| |_ ___  _ __ ___
# | |  _ / _ \ '_ \ / _ \ '__/ _` | __/ _ \| '__/ __|
# | |_| |  __/ | | |  __/ | | ;(_| | || (_) | |  \__ \
#  \____|\___|_| |_|\___|_|  \__,_|\__\___/|_|  |___/

# libraries
import tcod as libtcod

# game files
import constants
import globalvars
import actor
import ai
import death
import magic

## globalvars.PLAYER
def player(coords):

    x, y = coords

    # create the player
    container_com = actor.CompContainers()

    creature_com = actor.CompCreature("Greg",
                                base_atk = 5,
                                max_hp = 50,
                                xp = 0,
                                death_function = death.player)

    globalvars.PLAYER = actor.ObjActor(x, y, "python",
                        animation_key = "A_globalvars.PLAYER",
                        animation_speed = 1,
                        creature = creature_com,
                        container = container_com)
    
    globalvars.PLAYER.level = 0

    globalvars.GAME.current_objects.append(globalvars.PLAYER)
    


# SPECIAL
def stairs(coords, downwards = True):
    x, y = coords
    if downwards:
        stairs_com = actor.CompStairs()
        stairs = actor.ObjActor(x, y, "stairs", 
                        animation_key = "S_STAIRS_DOWN", 
                        stairs = stairs_com)
    else:
        stairs_com = actor.CompStairs(downwards)
        stairs = actor.ObjActor(x, y, "stairs",
                        animation_key = 'S_STAIRS_UP', 
                        stairs = stairs_com)
        
    globalvars.GAME.current_objects.insert(-2, stairs)

def portal(coords):
    x, y = coords
    portal_com = actor.CompExitPortal()
    portal = actor.ObjActor(x, y, 'exit portal', animation_key = 'S_PORTALCLOSED', exitportal = portal_com)
    
    globalvars.GAME.current_objects.insert(-2, portal)

def LAMP(coords):
    
    x, y = coords
    
    item_com = actor.CompItem()
    
    return_object = actor.ObjActor(x, y, 'THE LAMP', animation_key = 'S_MAGIC_LAMP', item = item_com)

    globalvars.GAME.current_objects.insert(0, return_object)


# Items
def item(coords):
    
    random_num = libtcod.random_get_int(0, 1, 100)
    
    if random_num in range(1, 11): 
        new_item = scroll_lightning(coords)
        
    elif random_num in range(11, 21): 
        new_item = scroll_fireball_box(coords)
        
    elif random_num in range(21, 31): 
        new_item = scroll_confusion(coords)
        
    elif random_num in range(31, 36): 
        new_item = scroll_fireball_diamond(coords)
    
    elif random_num in range(36, 46):
        new_item = weapon_sword(coords)
        
    elif random_num in range(46, 56):
        new_item = armor_shield(coords)
        
    elif random_num in range(56, 66):
        new_item = weapon_dagger(coords)

    elif random_num in range(66, 71):
        new_item = weapon_scythe(coords)
    
    elif random_num in range(71, 81):   
        new_item = armor_shield(coords)
        
    elif random_num in range(81, 86):   
        new_item = armor_shield_diamond(coords)
        
    elif random_num in range(86, 91):   
        new_item = armor_body_diamond(coords)

    elif random_num in range(91, 101):   
        new_item = armor_body(coords)
        
    globalvars.GAME.current_objects.insert(0, new_item)

def scroll_lightning(coords):

    x, y = coords

    damage = libtcod.random_get_int(0, 8, 10)
    m_range = libtcod.random_get_int(0, 8, 9)
    

    item_com = actor.CompItem(use_function = magic.cast_lighting, value = (damage, m_range))
    
    return_object = actor.ObjActor(x, y, "Lightning scroll", animation_key = "S_SCROLL_01", item = item_com)
    
    return return_object

def scroll_fireball_box(coords):

    x, y = coords

    damage = libtcod.random_get_int(0, 6, 8)
    radius = 1
    m_range = libtcod.random_get_int(0, 7, 8)
    

    item_com = actor.CompItem(use_function = magic.cast_fireball_box, value = (damage, radius, m_range))
    
    return_object = actor.ObjActor(x, y, "Fireball-box scroll", animation_key = "S_SCROLL_02", item = item_com)
    
    return return_object

def scroll_fireball_diamond(coords):

    x, y = coords

    damage = libtcod.random_get_int(0, 7, 10)
    radius = 2
    m_range = libtcod.random_get_int(0, 5, 9)
    

    item_com = actor.CompItem(use_function = magic.cast_fireball_diamond, value = (damage, radius, m_range))
    
    return_object = actor.ObjActor(x, y, "Fireball-diamond scroll", animation_key = "S_SCROLL_04", item = item_com)
    
    return return_object

def scroll_confusion(coords):

    x, y = coords

    effect_length = libtcod.random_get_int(0, 5, 8) 

    item_com = actor.CompItem(use_function = magic.cast_confusion, value = effect_length)
    
    return_object = actor.ObjActor(x, y, "Confusion scroll", animation_key = "S_SCROLL_03", item = item_com)
    
    return return_object

def weapon_sword(coords):
    x, y = coords
    
    bonus = libtcod.random_get_int(0, 4, 6)
    
    equipment_com = actor.CompEquipment(attack_bonus = bonus, slot = "hand_right")
    
    return_object = actor.ObjActor(x, y, "Sword", animation_key = "S_SWORD", equipment = equipment_com)
    
    return return_object

def weapon_scythe(coords):
    x, y = coords
    
    bonus = libtcod.random_get_int(0, 10, 15)
    
    equipment_com = actor.CompEquipment(attack_bonus = bonus, slot = "hand_right")
    
    return_object = actor.ObjActor(x, y, "Scythe", animation_key = "S_LONG_SWORD", equipment = equipment_com)
    
    return return_object

def weapon_dagger(coords):
    x, y = coords
    
    bonus = libtcod.random_get_int(0, 2, 5)
    
    equipment_com = actor.CompEquipment(attack_bonus = bonus, slot = "hand_right")
    
    return_object = actor.ObjActor(x, y, "Dagger", animation_key = "S_DAGGER", equipment = equipment_com)
    
    return return_object

def armor_shield_diamond(coords):
    x, y = coords
    
    bonus = libtcod.random_get_int(0, 8, 12)
    
    equipment_com = actor.CompEquipment(defense_bonus = bonus, slot = "hand_left")
    
    return_object = actor.ObjActor(x, y, "Diamond shield", animation_key = "S_STRONG_SHIELD", equipment = equipment_com)
    
    return return_object

def armor_shield(coords):
    x, y = coords
    
    bonus = libtcod.random_get_int(0, 2, 5)
    
    equipment_com = actor.CompEquipment(defense_bonus = bonus, slot = "hand_left")
    
    return_object = actor.ObjActor(x, y, "Shield", animation_key = "S_SHIELD", equipment = equipment_com)
    
    return return_object

def armor_body(coords):
    x, y = coords
    
    bonus = 4
    
    equipment_com = actor.CompEquipment(defense_bonus = bonus, slot = "body")
    
    return_object = actor.ObjActor(x, y, "Armor", animation_key = "S_ARMOR", equipment = equipment_com)
    
    return return_object

def armor_body_diamond(coords):
    x, y = coords
    
    bonus = 8
    
    equipment_com = actor.CompEquipment(defense_bonus = bonus, slot = "body")
    
    return_object = actor.ObjActor(x, y, "Diamond armor", animation_key = "S_STRONG_ARMOR", equipment = equipment_com)
    
    return return_object


# Enemies
def enemy(coords):
    random_num = libtcod.random_get_int(0, 1, 100)
    
    if random_num in range(1, 16): 
        new_enemy = snake_cobra(coords)
        
    elif random_num in range(16, 51): 
        new_enemy = snake_anaconda(coords)
        
    elif random_num in range(51, 101): 
        new_enemy = mouse(coords)
        
    elif random_num in range(150, 200): 
        new_enemy = snake_cobra(coords)
        
    globalvars.GAME.current_objects.insert(-1, new_enemy)
    
    
def snake_anaconda(coords):
    
    x, y = coords
    
    max_health = libtcod.random_get_int(0, 5, 8)
    base_attack = libtcod.random_get_int(0, 2, 4)
    
    creature_name = libtcod.namegen_generate('Celtic female')
    
    creature_com = actor.CompCreature(creature_name, death_function = death.snake, 
                                base_atk = base_attack, max_hp = max_health, xp = (max_health + base_attack)// 2)
    
    ai_com = ai.Chase()
    snake = actor.ObjActor(x, y, "Anaconda", 
                    animation_key = "A_SNAKE_01", 
                    animation_speed = 1, 
                    creature = creature_com, 
                    ai= ai_com)
    
    return snake
    
def snake_cobra(coords):

    x, y = coords
    
    max_health = libtcod.random_get_int(0, 15, 20)
    base_attack = libtcod.random_get_int(0, 5, 8)
    
    creature_name = libtcod.namegen_generate('Celtic male')
    
    creature_com = actor.CompCreature(creature_name,death_function = death.snake, 
                                base_atk = base_attack, max_hp = max_health, xp = (max_health + base_attack)// 2)
    
    ai_com = ai.Chase()
    snake = actor.ObjActor(x, y, "Cobra", 
                    animation_key = "A_SNAKE_02", 
                    animation_speed = 1, 
                    creature = creature_com, 
                    ai= ai_com)
    
    return snake

def mouse(coords):
    x, y = coords
    
    max_health = 1
    base_attack = 0
    
    creature_name = libtcod.namegen_generate('Celtic male')
    
    creature_com = actor.CompCreature(creature_name,death_function = death.mouse, 
                                base_atk = base_attack, max_hp = max_health, xp = -2)
    
    ai_com = ai.Flee()
    
    item_com = actor.CompItem(use_function = magic.cast_heal, value = 3)
    
    mouse = actor.ObjActor(x, y, "mouse", 
                    animation_key = "A_MOUSE", 
                    animation_speed = 1, 
                    creature = creature_com, 
                    ai= ai_com,
                    item = item_com)
    
    return mouse
