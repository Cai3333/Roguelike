
#   ____ ___  __  __ ____   ___  _   _ _____ _   _ _____ ____  
#  / ___/ _ \|  \/  |  _ \ / _ \| \ | | ____| \ | |_   _/ ___| 
# | |  | | | | |\/| | |_) | | | |  \| |  _| |  \| | | | \___ \ 
# | |__| |_| | |  | |  __/| |_| | |\  | |___| |\  | | |  ___) |
#  \____\___/|_|  |_|_|    \___/|_| \_|_____|_| \_| |_| |____/ 

import math
import os
import datetime


import pygame
import tcod as libtcod

import constants
import game 
import globalvars
import maps
import text


class ObjActor:
    '''The actor object represents every entity in the game.
    This object is anything that can appear or act within the game.  Each entity 
    is made up of components that control how these objects work.
    Attributes:
        x (arg, int): position on the x axis
        y (arg, int): position on the y axis
        name_object (arg, str) : name of the object type, "chair" or
            "goblin" for example.
        animation (arg, list): sequence of images that make up the object's
            spritesheet. Created within the struc_Assets class.
        animation_speed (arg, float): time in seconds it takes to loop through
            the object animation.
    Components:
        creature: any object that has health, and generally can fight.
        ai: set of instructions an ObjActor can follow.
        container: objects that can hold an inventory.
        item: items are items that are able to be picked up and (usually) 
            usable.
    
    '''
    def __init__(self, x, y,
                name_object,
                animation_key,
                animation_speed = .5,
                depth = 0,
                state = None,

                # Components
                creature = None,
                ai = None,
                container = None,
                item = None,
                equipment = None,
                stairs = None,
                exitportal = None):
        
        self.x, self.y = x, y  # Map addres
        self.name_object = name_object
        self.animation_key = animation_key
        self.animation = globalvars.ASSETS.animation_dict[self.animation_key]
        self.animation_speed = animation_speed / 1.0 # in seconds
        self.state = state
        
        # speed -> frames conversion
        self._flickerspeed = self.animation_speed / len(self.animation)
        
        # time for deciding when to flip the image
        self._flickertimer = 0.0
        
        # currently viewed sprite
        self._spriteimage = 0
        
        self.creature = creature
        if self.creature:
            self.creature.owner = self

        self.ai = ai
        if self.ai:
            self.ai.owner = self
        
        self.container = container
        if self.container:
            self.container.owner = self
        
        self.item = item
        if self.item:
            self.item.owner = self
        
        self.equipment = equipment
        if self.equipment:
            self.equipment.owner = self
            
            self.item = CompItem()
            self.item.owner = self
            
        self.stairs = stairs
        if self.stairs:
            self.stairs.owner = self
            
        self.exitportal = exitportal
        if self.exitportal:
            self.exitportal.owner = self
            
            
    @property
    def display_name(self):
        if self.creature:
            return (self.creature.name_instance + " the " + self.name_object)
        
        if self.item:
            if self.equipment and self.equipment.equipped:
                return (self.name_object + "  (E)")
            else:
                return self.name_object
        
    def draw(self):
        '''Draws the object to the screen.
        This function draws the object to the screen if it appears within the 
        PLAYER fov.  It also keeps track of the timing for animations to trigger
        a transition to the next sprite in the animation.
        '''
        
        is_visible = libtcod.map_is_in_fov(globalvars.FOV_MAP, self.x, self.y)
        # draw the character if is visible
        if is_visible: # if visible, check to see if animation has > 1 image
            if len(self.animation) == 1:
                globalvars.SURFACE_MAP.blit(self.animation[0], (self.x * constants.CELL_WIDTH, self.y * constants.CELL_HEIGHT))
            
            # does this object have multiple sprites?
            elif len(self.animation) > 1:
                # only update animation timer if we can calculate how quickly
                # the game is running.
                if globalvars.CLOCK.get_fps() > 0.0:
                    self._flickertimer += 1 / globalvars.CLOCK.get_fps()
                
                # if the timer has reached the speed
                if self._flickertimer >= self._flickerspeed:
                    self._flickertimer = 0.0  # reset the timer
                    
                    # is this sprite the final item in the list?
                    if self._spriteimage >= len(self.animation) - 1:
                        self._spriteimage = 0 # reset sprite to top of list
                        
                    else:
                        self._spriteimage += 1 # advance to next sprite
                        
                globalvars.SURFACE_MAP.blit(self.animation[self._spriteimage], 
                                (self.x*constants.CELL_WIDTH, self.y*constants.CELL_HEIGHT))
    
    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        
        return math.sqrt(dx ** 2 + dy ** 2)
                    
    def move_towards(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        
        distance = math.sqrt(dx ** 2 + dy ** 2)
        
        dx = int(round(dx / distance))
        dy = int(round(dy / distance))
        
        self.creature.move(dx, dy)
        
    def move_away(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        
        distance = math.sqrt(dx ** 2 + dy ** 2)
        
        dx = int(round(dx / distance))
        dy = int(round(dy / distance))
        
        self.creature.move(dx, dy)
    
    def animation_destroy(self):
        self.animation = None
        
    def animation_init(self):
        self.animation = globalvars.ASSETS.animation_dict[self.animation_key]

class CompCreature:
    '''Creatures are actors that have health and can fight.
    Attributes:
        name_instance (arg, str): name of instance. "Bob" for example.
        max_hp (arg, int): max health of the creature.
        death_function (arg, function): function to be executed when hp reaches 0.
        current_hp (int): current health of the creature.
    '''
    def __init__(self, name_instance, base_atk = 2, base_def = 0, max_hp = 10, death_function = None):
        
        self.name_instance = name_instance
        self.base_atk = base_atk
        self.base_def = base_def
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.death_function = death_function
        
    
    def move(self, dx, dy):
        '''Moves the object
        
        Args: 
            dx (int): distance to move actor along x axis
            dy (int): distance to move actor along y axis
        '''
        
        # Is a wall if block_path is true
        tile_is_wall = (globalvars.GAME.current_map[self.owner.x + dx][self.owner.y +dy].block_path == True)
        
        target = maps.check_for_creature(self.owner.x + dx, self.owner.y + dy, self.owner)
        
        if target:
            self.attack(target)
        
        # Move if current position plus new position is not wall
        if not tile_is_wall and target is None:
            self.owner.x += dx
            self.owner.y += dy
    
    
    def attack(self, target):
        '''Creature makes an attack against another ObjActor
        
        Args:
            target (ObjActor): target to be attacked, must have creature 
                component.
            damage (int): amount of damage to be done to target
        '''
        
        damage_delt = self.power - target.creature.defense
        
        if damage_delt > 0 and self.owner is globalvars.PLAYER:
            pygame.mixer.Sound.play(globalvars.RANDOM_ENGINE.choice(globalvars.ASSETS.snd_list_hit))
        
        if damage_delt < 0:
            damage_delt = 0
            
        game.message(f"{self.name_instance} attacks {target.creature.name_instance} for {str(damage_delt)} damage!", constants.COLOR_WHITE)
            
        target.creature.take_damage(damage_delt)
            
    
    def take_damage(self, damage):
        """Applies damage received to self.health
        This function applies damage to the ObjActor with the creature 
        component.  If the current health level falls below 1, executes the 
        death_function.
        
        Args:
            damage (int): amount of damage to be applied to self.
        """
        # subtract health
        if damage < 0:
            damage = 0
            
        self.current_hp -= damage
        
        if self.current_hp < 0:
            self.current_hp = 0
        
        # print message
        
        game.message(f"{self.name_instance}'s health is {str(self.current_hp)}/{str(self.max_hp)}.", constants.COLOR_RED)
        
        # if health now equals < 1, execute death function
        if self.current_hp <= 0:
            if self.death_function is not None:
                self.death_function(self.owner)
    
    def heal(self, value):
        self.current_hp += value
        
        if self.current_hp > self.max_hp:
            self.current_hp = self.max_hp

    def draw_health(self):
        
        self.hp_percentage = self.current_hp / self.max_hp 
        
        if self.hp_percentage >= 0.8:
            col = constants.COLOR_GREEN
        elif self.hp_percentage >= 0.6:
            col = (167, 255, 0) 
        elif self.hp_percentage >= 0.4:
            col = (255, 255, 0)
        elif self.hp_percentage >= 0.2:
            col = (255, 165, 0)
        elif self.hp_percentage >= 0.0:
            col = constants.COLOR_RED
        
        if self.hp_percentage < 0:
            self.hp_percentage = 0 
            
        BAR_LENGTH = 100
        BAR_HEIGHT = 20
        fill = self.hp_percentage * BAR_LENGTH
        
        ouline_rect = pygame.Rect(40, 10, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(40, 10, fill, BAR_HEIGHT)
        
        pygame.draw.rect(globalvars.SURFACE_MAIN, col, fill_rect)
        pygame.draw.rect(globalvars.SURFACE_MAIN, constants.COLOR_WHITE, ouline_rect, 2)
        text.display(globalvars.SURFACE_MAIN, "HP", constants.FONT_DEBUG_MESSAGE, (4,10), constants.COLOR_WHITE)
        
    
    @property
    def power(self):
        total_power = self.base_atk
        
        if self.owner.container:
            object_bonuses = [obj.equipment.attack_bonus 
                            for obj in self.owner.container.equipped_items]

            for bonus in object_bonuses:
                if bonus:
                    total_power += bonus
        return total_power
    
    @property
    def defense(self):
        total_defense = self.base_def
        
        if self.owner.container:
            object_bonuses = [obj.equipment.defense_bonus 
                            for obj in self.owner.container.equipped_items]

            for bonus in object_bonuses:
                if bonus:
                    total_defense += bonus
        
        return total_defense

class CompContainers:
    
    def __init__(self, volume = 10.0, inventory = None):
        self.inventory = inventory
        self.max_volume = volume
        
        if inventory:
            self.inventory = inventory
        else: 
            self.inventory = []
        
    ## TODO Get Names of everything in inventory
    
    ## TODO Get volume within container
    @property
    def volume(self):
        return 0.0

    @property
    def equipped_items(self):
        
        list_of_equipped_items = [obj for obj in self.inventory 
                                if obj.equipment and obj.equipment.equipped]
        
        return list_of_equipped_items
    
    ## TODO Get weight of everything in inventory

class CompItem:
    '''Items are components that can be picked up and used.
    Attributes:
        weight (arg, float): how much does the item weigh
        volume (arg, float): how much space does the item take up
    '''
    
    def __init__(self, weight = 0.0, volume = 0.0, use_function = None, value = None):
        self.weight = weight
        self.volume = volume
        self.value = value
        self.use_function = use_function
        
    def pick_up(self, actor):
        '''The item is picked up and placed into an object's inventory.
        When called, this method seeks to place the item into an object's 
        inventory if there is room.  It then removes the item from a Game's 
        current_objects list.
        Args:
            actor (ObjActor): the object that is picking up the item.
        '''
        
        if actor.container: # first, checks for container component
            
            # does the container have room for this object?
            if actor.container.volume + self.volume > actor.container.max_volume:
                
                # if no, print error message
                game.message("Not enough room to pick up")
                
            else:
                
                # otherwise, pick the item up, remove from GAME.current_objects
                # message the player
                game.message("Picking up")
                
                # add to actor inventory
                actor.container.inventory.append(self.owner)
                self.owner.animation_destroy()
                        
                # remove from game active list
                globalvars.GAME.current_objects.remove(self.owner)
                
                # tell item what container holds it
                self.current_container = actor.container

    def drop(self, new_x, new_y):
        '''Drops the item onto the ground.
        This method removes the item from the actor.container inventory and 
        places it into the GAME.current_objects list.  Drops the item at the
        location defined in the args.
        Args:
            new_x (int): x coord on the map to drop item
            new_y (int): y coord on the map to drop item
        '''
        
        # add this item to tracked objects
        globalvars.GAME.current_objects.insert(-1, self.owner)
        
        self.owner.animation_init()
        
        # remove from the inventory of whatever actor holds it
        self.current_container.inventory.remove(self.owner)
        
        # set item location to as defined in the args
        self.owner.x = new_x
        self.owner.y = new_y
        
        # confirm successful placement with game message
        game.message("Item dropped!")
    
    def use(self):
        '''Use the item by producing an effect and removing it
        
        '''
        
        if self.owner.equipment:
            self.owner.equipment.toggle_equip()
            return 
            
        
        if self.use_function:
            result = self.use_function(self.current_container.owner, self.value)
    
            if result is not None:
                print("use function failed")

            else:
                self.current_container.inventory.remove(self.owner)

class CompEquipment:
    def __init__(self, attack_bonus = None, defense_bonus = None, slot = None):
        self.attack_bonus = attack_bonus
        self.defense_bonus = defense_bonus
        self.slot = slot
        
        self.equipped = False
    
    def toggle_equip(self):
        if self.equipped:
            self.unequip()
        else:
            self.equip()
        
    def equip(self):
        # Check for equipment in slot
        all_equipped_items = self.owner.item.current_container.equipped_items
        
        for item in all_equipped_items:
            if item.equipment.slot and (item.equipment.slot == self.slot):
                game.message("Equipment slot is occupied", constants.COLOR_RED)
                return
                
        
        self.equipped = True
        
        game.message("item equipped")
        
    def unequip(self):
        self.equipped = False
        game.message("item unequipped")
        
class CompStairs:
    def __init__(self, downwards = True):
        self.downwards = downwards
        
    def use(self):
        if self.downwards:
            globalvars.GAME.transition_next()
            
        else:
            globalvars.GAME.transition_previous()        

class CompExitPortal:
    def __init__(self):
        self.OPENANIMATION = "S_PORTALOPEN"
        self.CLOSEDANIMATION = "S_PORTALCLOSED"

    def update(self):
        # flag initialization
        found_lamp = False

        # check conditions
        portal_open = self.owner.state == "OPEN"

        for obj in globalvars.PLAYER.container.inventory:
            if obj.name_object == "THE LAMP":
                found_lamp = True

        if found_lamp and not portal_open:
            self.owner.state = "OPEN"
            self.owner.animation_key = self.OPENANIMATION
            self.owner.animation_init()

        if not found_lamp and portal_open:
            self.owner.state = "CLOSED"
            self.owner.animation_key = self.CLOSEDANIMATION
            self.owner.animation_init()
    
    def use(self):
        if self.owner.state == 'OPEN':
            
            globalvars.PLAYER.state = "STATUS_WIN"
            
            globalvars.SURFACE_MAIN.fill(constants.COLOR_WHITE)
            
            screen_center = (constants.CAMERA_WIDTH / 2, constants.CAMERA_HEIGHT / 2)

            text.display(globalvars.SURFACE_MAIN, "YOU WON!", constants.FONT_TITLE_SCREEN, screen_center, constants.COLOR_BLACK, center = True)
            
            pygame.display.update()
            
            filename = "data\winrecord_" + globalvars.PLAYER.creature.name_instance + '.' + datetime.date.today().strftime('%d%B%Y') + (".txt")
            
            file_exists = os.path.isfile(filename)
            save_exists = os.path.isfile('data/savegame')
            
            if file_exists: os.remove(filename)
            if save_exists: os.remove('data/savegame')
            
            legacy_file = open(filename, 'a+')
            
            legacy_file.write('*************THIS CHARACTER WON**************' + '\n')
            
            for message, color in globalvars.GAME.message_history:
                legacy_file.write(message + "\n")
            legacy_file.write("\n*****************END_FILE*******************\n\n\n")

            pygame.time.wait(2000)