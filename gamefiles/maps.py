#  __  __             
# |  \/  | __ _ _ __  
# | |\/| |/ _` | '_ \ 
# | |  | | (_| | |_) |
# |_|  |_|\__,_| .__/ 
#              |_| 

import tcod as libtcod

# game files
import globalvars
import constants
import data
import generator

            
class ObjRoom:
    '''This is a rectangle that lives on the map'''
    
    def __init__(self, coords, size):
        self.x1, self.y1 = coords
        self.w, self.h = size
        
        self.x2 = self.x1 + self.w
        self.y2 = self.y1 + self.h
        
    @property
    def center(self):
        center_x = (self.x1 + self.x2) // 2
        center_y = (self.y1 + self.y2) // 2
        
        return (center_x, center_y)
        
    def intersect(self, other):
        # Return True if other obj intersects with this one
        objects_intersect = (self.x1 <= other.x2 and self.x2 >= other.x1 and 
                            self.y1 <= other.y2 and self.y2 >= other.y1)
        return objects_intersect
    

def create():
    '''Creates the default map.
    Currently, the map this function creatures is a small room with 2 pillars 
    within it.  It is a testing map.
    Returns:
        new_map (array): This array is populated with struc_Tile objects.
    Effects:
        Calls make_fov on new_map to preemptively create the fov.
    '''
    
    # initializes an empty map
    new_map = [[data.StrucTile(True) for y in range(0, constants.MAP_HEIGHT)]
                                    for x in range(0, constants.MAP_WIDTH)]

    # generate new room
    list_of_rooms = []

    for i in range(constants.MAP_MAX_NUM_ROOMS):

        w = libtcod.random_get_int(0, constants.ROOM_MIN_WIDTH,
                                    constants.ROOM_MAX_WIDTH)
        h = libtcod.random_get_int(0, constants.ROOM_MIN_HEIGHT,
                                    constants.ROOM_MAX_HEIGHT)

        x = libtcod.random_get_int(0, 2, constants.MAP_WIDTH - w - 2)
        y = libtcod.random_get_int(0, 2, constants.MAP_HEIGHT - h - 2)

        #create the room
        new_room = ObjRoom((x, y), (w, h))

        failed = False

        # check for interference
        for other_room in list_of_rooms:
            if new_room.intersect(other_room):
                failed = True
                break

        if not failed:
            # place room
            create_room(new_map, new_room)
            current_center = new_room.center

            if len(list_of_rooms) != 0:

                previous_center = list_of_rooms[-1].center

                # dig tunnels
                create_tunnels(current_center, previous_center, new_map)

            list_of_rooms.append(new_room)

    # create FOV_MAP
    make_fov(new_map)

    # returns the created map
    return (new_map, list_of_rooms)

def place_objects(room_list):
    
    current_level = len(globalvars.GAME.map_previous) + 1
    
    top_level = (current_level == 1)
    
    final_level = (current_level == constants.MAP_NUM_LEVELS)
    
    
    for room in room_list:
        first_room = (room == room_list[0])
        last_room = (room == room_list[-1])
        
        if first_room:
            globalvars.PLAYER.x, globalvars.PLAYER.y = room.center
        
        if first_room and top_level:
            generator.portal(room.center)
        
        if first_room and not top_level:
            generator.stairs((globalvars.PLAYER.x, globalvars.PLAYER.y), downwards = False)
            
        if last_room:
            if final_level:
                generator.LAMP(room.center)
                lampx, lampy = room.center
            else:
                generator.stairs(room.center)
                stairsx, stairsy = room.center
            
        x = libtcod.random_get_int(0, room.x1, room.x2 -1)
        y = libtcod.random_get_int(0, room.y1, room.y2 -1)
        
        if (x, y) != (globalvars.PLAYER.x, globalvars.PLAYER.y):
            generator.enemy((x, y))
            
        x2 = libtcod.random_get_int(0, room.x1, room.x2 -1)
        y2 = libtcod.random_get_int(0, room.y1, room.y2 -1)
        
        if (x2, y2) != (globalvars.PLAYER.x, globalvars.PLAYER.y) and (x2, y2) != (x, y):
            if last_room:
                if final_level and (x2, y2) != (lampx, lampy):
                    generator.item((x2, y2))
                else:
                    if (x2, y2) != (stairsx, stairsy):
                        generator.item((x2, y2))
            else:
                generator.item((x2, y2))

def create_room(new_map, new_room):
    
    for x in range(new_room.x1, new_room.x2):
        for y in range(new_room.y1, new_room.y2):
            
            new_map[x][y].block_path = False
            
def create_tunnels(coords1, coords2, new_map):
    coin_flip = (libtcod.random_get_int(0, 0, 1) == 1)
    
    x1, y1 = coords1
    x2, y2 = coords2

    if coin_flip:
        
        for x in range(min(x1, x2), max(x1, x2) + 1):
            new_map[x][y1].block_path = False
            
        for y in range(min(y1, y2), max(y1, y2) + 1):
            new_map[x2][y].block_path = False
            
    else: 
        
        for y in range(min(y1, y2), max(y1, y2) + 1):
            new_map[x1][y].block_path = False

        for x in range(min(x1, x2), max(x1, x2) + 1):
            new_map[x][y2].block_path = False
        
def check_for_creature(xPos, yPos, exclude_object = None):
    '''Check the current map for creatures at specified location.
    This function looks at that location for any object that has a creature
    component and returns it.  Optional argument allows user to exclude an 
    object from the search, usually the Player
    Args:
        x (int): x map coord to check for creature
        y (int): y map coord to check for creature
        exclude_object(ObjActor, optional): if an object is passed into this 
            function, this object will be ignored by the search.
    Returns: 
        target (ObjActor): but only if found at the location specified in the 
            arguments and if not excluded.
    '''
    
    # check objectlist to find creature at that location that isn't excluded
    for obj in globalvars.GAME.current_objects:
        if (obj is not exclude_object and 
            obj.x == xPos and 
            obj.y == yPos and 
            obj.creature):
                return obj
    return None


    
def make_fov(incoming_map):
    '''Creates an FOV map based on a map.
    Args:
        incoming_map (array): map, usually created with create
    Effects:
        generates the FOV_MAP
    '''
    
    globalvars.FOV_MAP = libtcod.map.Map(constants.MAP_WIDTH, constants.MAP_HEIGHT)
    
    for y in range(constants.MAP_HEIGHT):
        for x in range(constants.MAP_WIDTH):
            libtcod.map_set_properties(globalvars.FOV_MAP, x, y,
                not incoming_map[x][y].block_path, not incoming_map[x][y].block_path)
    
def calculate_fov():
    '''Calculates the FOV based on the Player's perspective.
    Accesses the global variable FOV_CALCULATE, if FOV_CALCULATE is True, sets 
    it to False and recalculates the FOV.
    '''    

    
    if globalvars.FOV_CALCULATE:
        # reset FOV_CALCULATE
        FOV_CALCULATE = False
        
        # run the calculation function
        libtcod.map.Map.compute_fov(globalvars.FOV_MAP, globalvars.PLAYER.x, globalvars.PLAYER.y, constants.TORCH_RADIUS, constants.FOV_LIGHT_WALLS,
            constants.FOV_ALGO)

def objects_at_coords(coords_x, coords_y):
    '''Get a list of every object at a coordinate.
    Args: 
        coords_x (int): x axis map coordinate of current map to check
        coords_y (int): y axis map coordinate of current map to check
    Returns:
        object_options (list): list of every object at the coordinate.
    '''    
    
    object_options = [obj for obj in globalvars.GAME.current_objects
                        if obj.x == coords_x and obj.y == coords_y] 
    return object_options

def find_line(coords1, coords2):
    '''Converts two x, y coords into a list of tiles.
    coords1 : (x1, y1)
    coords2 : (x2, y2)
    '''
    
    x1, y1 = coords1
    
    x2, y2 = coords2
    
    libtcod.line_init(x1, y1, x2, y2)
    
    calc_x, calc_y = libtcod.line_step()
    
    coord_list = []
    
    if x1 == x2 and y1 == y2:
        return [(x1, y1)]
    
    while (not calc_x is None):
        coord_list.append((calc_x, calc_y))
        
        calc_x, calc_y = libtcod.line_step()
        
    return coord_list
        
def find_radius_box(coords, radius):

    center_x, center_y = coords
    
    tile_list = []
    
    start_x = (center_x - radius)
    end_x = (center_x + radius + 1)
    
    start_y = (center_y - radius) 
    end_y = (center_y + radius + 1)
    
    for x in range(start_x, end_x):
        for y in range(start_y, end_y):
            tile_list.append((x, y))
    return tile_list

def find_radius_diamond(coords, radius):

    tile_x, tile_y = coords
    
    list_of_tiles = []
    
    list_of_tiles.append((tile_x,tile_y))
    for i in range(1,radius+1):
        list_of_tiles.append((tile_x+i,tile_y))
        list_of_tiles.append((tile_x-i,tile_y))
        list_of_tiles.append((tile_x,tile_y-i))
        list_of_tiles.append((tile_x,tile_y+i))
        
    vertical = radius-1
    horizontal = 1
    temp_horizontal = horizontal
    
    for a in range(vertical):
        while(temp_horizontal != 0):
            list_of_tiles.append((tile_x+temp_horizontal,tile_y-vertical))
            list_of_tiles.append((tile_x-temp_horizontal,tile_y-vertical))   
            list_of_tiles.append((tile_x+temp_horizontal,tile_y+vertical))
            list_of_tiles.append((tile_x-temp_horizontal,tile_y+vertical))
            temp_horizontal -= 1
            
        vertical -= 1
        horizontal += 1
        temp_horizontal = horizontal
    return list_of_tiles
