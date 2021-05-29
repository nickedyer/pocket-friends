"""
Launch script for Pocket Friends.
"""
import pygame
import sys
from pocket_friends.game import main as game_main
from pocket_friends.development.dev_menu import main as dev_menu_main

enable_dev = False

if __name__ == '__main__':

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
