import os
from pathlib import Path
import argparse
import pygame
import sys
from pocket_friends.game_files.game import main as game_main


def main():
    """
    Launch script for Pocket Friends.
    """

    # Creates the parser object.
    parser = argparse.ArgumentParser()

    # Adds parser arguments.
    parser.add_argument('-D', '--delete-save', action='store_true', help='Deletes the save file if it exists.')
    parser.add_argument('-s', '--size', type=int, default=320, help='Sets the size of the window.')

    # Parse the arguments given
    args = parser.parse_args()

    # If given the delete-save argument, delete the safe file
    if args.delete_save:
        save_dir = os.path.join(Path.home(), '.pocket_friends')
        # Remove the file if it exists
        try:
            os.remove(save_dir + '/save.json')
            print('Save file deleted.')
        except FileNotFoundError:
            print('Save file does not exist, cannot delete.')

    # Set the screen size
    screen_size = int(args.size)

    # Start the game
    game_main(screen_size)

    # Cleanup
    pygame.quit()
    sys.exit()