"""
Launch script for Pocket Friends.
"""
import pygame
import sys
from pocket_friends.game_files.game import main as game_main
from pocket_friends.development.dev_menu import main as dev_menu_main

__version__ = '0.0.1'

if __name__ == '__main__':
    enable_dev = False

    # enable dev mode if --dev argument is passed
    if len(sys.argv) > 0:
        for args in sys.argv:
            if args == '--dev':
                enable_dev = True

    if not enable_dev:
        game_main()
    else:
        dev_menu_main()

    pygame.quit()
    sys.exit()