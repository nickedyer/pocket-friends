"""
Launch script for Pocket Friends.
"""
import os
from pathlib import Path
import pygame
import sys
from pocket_friends.game_files.game import main as game_main
from pocket_friends.development.dev_menu import main as dev_menu_main

if __name__ == '__main__':
    enable_dev = False

    # enable dev mode if --dev argument is passed
    if len(sys.argv) > 0:
        for args in sys.argv:
            if args == '--dev':
                enable_dev = True
            if args == '--delete-save':
                save_dir = os.path.join(Path.home(), '.pocket_friends')
                os.remove(save_dir + '/save.json')


    if not enable_dev:
        game_main()
    else:
        dev_menu_main()

    pygame.quit()
    sys.exit()
