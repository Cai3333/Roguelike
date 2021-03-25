
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
                                speed = constants.PLAYER_SPEED,
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

    item_chances = {}
    
    item_chances['ligthing'] = from_dungeon_level([[3, 2], [8, 4], [6, 6], [4, 8]])
    
    item_chances['fireball_box'] = from_dungeon_level([[3, 1], [5, 3], [6, 6], [2, 8]])
    
    item_chances['confusion'] = 5
    
    item_chances['fireball_diamond'] = from_dungeon_level([[6, 4], [10, 6], [15, 8]])
    
    item_chances['sword'] = from_dungeon_level([[10, 1], [7, 3], [5, 6], [3, 8]])
    
    item_chances['shield'] = from_dungeon_level([[10, 1], [7, 3], [5, 6], [3, 8]])
    
    item_chances['dagger'] = from_dungeon_level([[15, 2], [5, 4], [1, 6]])
    
    item_chances['scythe'] = from_dungeon_level([[10, 5], [15, 8]])
    
    item_chances['shield_diamond'] = from_dungeon_level([[10, 5], [15, 8]])
    
    item_chances['body_diamond'] = from_dungeon_level([[10, 5], [15, 8]])
    
    item_chances['body'] = from_dungeon_level([[10, 1], [7, 3], [5, 6], [3, 8]])
    
    choice = random_choice(item_chances)
    
    new_item = None
    
    if choice == 'lighting': 
        new_item = scroll_lightning(coords)
        
    elif choice == 'fireball_box': 
        new_item = scroll_fireball_box(coords)
        
    elif choice == 'confusion': 
        new_item = scroll_confusion(coords)
        
    elif choice == 'fireball_diamond': 
        new_item = scroll_fireball_diamond(coords)
    
    elif choice == 'sword':
        new_item = weapon_sword(coords)
        
    elif choice == 'shield':
        new_item = armor_shield(coords)
        
    elif choice == 'dagger':
        new_item = weapon_dagger(coords)

    elif choice == 'scythe':
        new_item = weapon_scythe(coords)
        
    elif choice == 'shield_diamond':   
        new_item = armor_shield_diamond(coords)
        
    elif choice == 'body_diamond':   
        new_item = armor_body_diamond(coords)

    elif choice == 'body':   
        new_item = armor_body(coords)
    
    if new_item:
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
    
    monster_chances = {}
    
    monster_chances['cobra'] = from_dungeon_level([[5, 2], [10, 4], [30, 6], [50, 8]])
    
    monster_chances['mouse'] = from_dungeon_level([[65, 1], [55, 3], [40, 6], [20, 8]])
    
    monster_chances['anaconda'] = 30
    
    choice = random_choice(monster_chances)
    
    if choice == 'cobra': 
        new_enemy = snake_cobra(coords)
        
    elif choice == 'anaconda': 
        new_enemy = snake_anaconda(coords)
        
    elif choice == 'mouse': 
        new_enemy = mouse(coords)
        
        
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
    
    creature_com = actor.CompCreature(creature_name, death_function = death.mouse, 
                                base_atk = base_attack, max_hp = max_health, xp = -2, speed = 20)
    
    ai_com = ai.Flee()
    
    item_com = actor.CompItem(use_function = magic.cast_heal, value = 3)
    
    mouse = actor.ObjActor(x, y, "mouse", 
                    animation_key = "A_MOUSE", 
                    animation_speed = 1, 
                    creature = creature_com, 
                    ai= ai_com,
                    item = item_com)
    
    return mouse

def random_choice_index(chances):  #choose one option from list of chances, returning its index
    #the dice will land on some number between 1 and the sum of the chances
    dice = libtcod.random_get_int(0, 1, sum(chances))

    #go through all chances, keeping the sum so far
    running_sum = 0
    choice = 0
    for w in chances:
        running_sum += w

        #see if the dice landed in the part that corresponds to this choice
        if dice <= running_sum:
            return choice
        choice += 1
        
def random_choice(chances_dict):
    #choose one option from dictionary of chances, returning its key
    chances = list(chances_dict.values())
    strings = list(chances_dict.keys())
    return strings[random_choice_index(chances)]

def from_dungeon_level(table):
    #returns a value that depends on level. the table specifies what value occurs after each level, default is 0.
    for (value, level) in reversed(table):
        if int(globalvars.GAME.current_level) >= level:
            return value
    return 0