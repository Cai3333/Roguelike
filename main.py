#  __  __    _    ___ _   _ 
# |  \/  |  / \  |_ _| \ | |
# | |\/| | / _ \  | ||  \| |
# | |  | |/ ___ \ | || |\  |
# |_|  |_/_/   \_\___|_| \_|

# add subdirectory to the path to import gamefiles
import sys
sys.path.insert(0, 'c:\Python\Projects\Roguelike\gamefiles')

# gamefiles
import startup
import menu

if __name__ == '__main__':
    menu.main()