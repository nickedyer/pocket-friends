"""
Development menu for the game on Raspberry Pi. NOTE: THIS DOES NOTHING ON A COMPUTER!
"""
import pocket_friends.game
import importlib.util
import os
import pygame
import time
from .button_test import button_test
from .menus import Menu
from ..gpio_handler import GPIOHandler, Constants

dev_version = '0.0.1'

try:
    importlib.util.find_spec('RPi.GPIO')
    import RPi.GPIO as GPIO
except ImportError:
    import pocket_friends.development.FakeGPIO as GPIO

# Global variable to keep track of the current menu.
menu = 'main'


def run_button_test():
    """
    Runs the GPIO button test.
    """
    GPIOHandler.teardown()
    button_test()
    GPIOHandler.setup()


def clear_screen():
    """
    Clears the screen.
    """
    print("\n" * 20)


def start_game():
    """
    Cleans the GPIO and starts the game.
    """
    GPIOHandler.teardown()
    pocket_friends.game.main()
    pygame.quit()
    GPIOHandler.setup()


def quit_menu():
    """
    Quits the menu.
    """
    exit(0)


def quit_with_error():
    """
    Quits the menu with error code 3.
    """
    exit(3)


def change_menu(new_menu):
    """
    Changes the global menu variable for the dev menu
    :param new_menu: the menu to change to
    """
    global menu
    menu = new_menu
    clear_screen()
    print('...')
    time.sleep(0.75)


def shutdown():
    """
    Shuts down the linux system.
    """
    os.system('sudo shutdown now')


def restart():
    """
    Restarts the linux system.
    """
    os.system('sudo reboot')


def main():
    """
    Starts the dev menu.
    """

    # The following defines all of the options in the various different menus.

    main_menu = Menu('Pocket Friends Dev Menu {0}\nGame Version {1}'.format(dev_version, pocket_friends.game.version))
    main_menu.add_option(Menu.Option('Start Game', start_game))
    main_menu.add_option(Menu.Option('Button Test', run_button_test))
    main_menu.add_option(Menu.Option('Restart Dev Menu', quit_with_error))
    main_menu.add_option(Menu.Option('Shutdown Pi', change_menu, 'shutdown'))
    main_menu.add_option(Menu.Option('Restart Pi', change_menu, 'restart'))
    main_menu.add_option(Menu.Option('Quit Dev Menu', change_menu, 'quit'))

    shutdown_confirm = Menu('Are you sure you want to shutdown?')
    shutdown_confirm.add_option(Menu.Option('No', change_menu, 'main'))
    shutdown_confirm.add_option(Menu.Option('Yes', shutdown))

    restart_confirm = Menu('Are you sure you want to restart?')
    restart_confirm.add_option(Menu.Option('No', change_menu, 'main'))
    restart_confirm.add_option(Menu.Option('Yes', restart))

    quit_confirm = Menu('Are you sure you want to exit?')
    quit_confirm.add_option(Menu.Option('No', change_menu, 'main'))
    quit_confirm.add_option(Menu.Option('Yes', quit_menu))

    GPIOHandler.setup()

    def menu_handler(current_menu):
        """
        Draws the menu and handles the GPIO inputs
        :param current_menu: the current menu being drawn on the screen
        """
        current_menu.draw_menu()

        while True:  # Main GPIO input loop

            # Limits how often the program checks for a GPIO input. Eases CPU usage.
            time.sleep(0.125)

            if GPIOHandler.get_press(Constants.buttons.get('j_d')):
                current_menu.select_next()
                break
            if GPIOHandler.get_press(Constants.buttons.get('j_u')):
                current_menu.select_prev()
                break
            if GPIOHandler.get_press(Constants.buttons.get('a')):
                current_menu.run_selection()
                break

    while True:  # Loop for drawing the menus.

        while menu == 'main':
            menu_handler(main_menu)

        while menu == 'shutdown':
            menu_handler(shutdown_confirm)

        while menu == 'restart':
            menu_handler(restart_confirm)

        while menu == 'quit':
            menu_handler(quit_confirm)
