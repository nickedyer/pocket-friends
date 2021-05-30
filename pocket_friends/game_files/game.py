"""
Main file for the entire hardware. Controls everything except for GPIO input.
"""
from collections import deque
import importlib.util
import json
import os
from pathlib import Path
import pocket_friends
import pygame
from pygame.locals import *
from ..hardware.gpio_handler import Constants, GPIOHandler

# FPS for the entire game to run at.
game_fps = 16

# Gets the directory of the script for importing and the save directory
script_dir = os.path.dirname(__file__)
save_dir = os.path.join(Path.home(), '.pocket_friends')

# Tries to make the save directory. Does nothing if it already exists.
try:
    os.mkdir(save_dir)
except FileExistsError:
    pass


class FileHandler:
    """
    Class that handles the hardware attributes and save files.
    """

    def __init__(self):
        # Attributes that are saved to a file to recover upon startup.
        self.attributes = {
            'time_elapsed': 0,
            'age': 0,
            'health': 0,
            'hunger': 0,
            'happiness': 0,
            'evolution_stage': -1,
        }

    def write_save(self):
        """
        Writes attributes of class to "save.json" file.
        """
        with open(save_dir + '/save.json', 'w') as save_file:
            json.dump(self.attributes, save_file)
            save_file.close()

    def read_save(self):
        """
        Reads from "save.json" and inserts into attributes dictionary. Creates file if it does not exist.
        """
        # Open up the save file and read it into self.attributes.
        try:
            with open(save_dir + '/save.json', 'r') as save_file:
                self.attributes = json.load(save_file)
                save_file.close()

        # If there is no save file, write one with the defaults.
        except FileNotFoundError:
            self.write_save()


class PlaygroundFriend(pygame.sprite.Sprite):
    """
    Class for the sprite of the creature on the main playground.
    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


class SelectionEgg(pygame.sprite.Sprite):
    """
    Class for the eggs on the egg selection screen.
    """

    def __init__(self, egg_color):
        pygame.sprite.Sprite.__init__(self)

        image_directory = script_dir + '/resources/images/egg_images/{0}'.format(egg_color)

        # Load the egg from the given color and get the bounding rectangle for the image.
        self.images = []
        for filename in os.listdir(image_directory):
            self.images.append(pygame.image.load(image_directory + '/' + filename))

        self.rect = self.images[0].get_rect()
        self.index = 0
        self.image = self.images[self.index]

        self.animation_frames = game_fps / len(self.images)
        self.current_frame = 0

    def update_frame_dependent(self):
        """
        Updates the image of Sprite every 6 frame (approximately every 0.1 second if frame rate is 60).
        """

        self.current_frame += 1
        if self.current_frame >= self.animation_frames:
            self.current_frame = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]

    def update(self):
        """This is the method that's being called when 'all_sprites.update(dt)' is called."""
        self.update_frame_dependent()


# Makes Pygame draw on the display of the RPi.
os.environ["SDL_FBDEV"] = "/dev/fb1"

# Useful for debugging on the PC. Imports a fake RPi.GPIO library if one is not found (which it can't
# be on a PC, RPi.GPIO cannot be installed outside of a Raspberry Pi.
try:
    importlib.util.find_spec('RPi.GPIO')
    import RPi.GPIO as GPIO
except ImportError:
    import pocket_friends.development.FakeGPIO as GPIO


def game():
    """
    Starts the hardware.
    """
    pygame.init()

    # Hide the cursor for the Pi display.
    pygame.mouse.set_visible(False)

    # The hardware is normally rendered at 80 pixels and upscaled from there. If changing displays, change the
    # screen_size to reflect what the resolution of the new display is.
    rendered_size = 80
    screen_size = 800

    window = pygame.display.set_mode((screen_size, screen_size))
    surface = pygame.Surface((rendered_size, rendered_size))

    # Only really useful for PCs. Does nothing on the Raspberry Pi.
    pygame.display.set_caption('Pocket Friends {0}'.format(pocket_friends.__version__))

    # Add an icon to the pygame window.
    icon = pygame.image.load(script_dir + '/resources/images/icon/icon.png').convert_alpha()
    pygame.display.set_icon(icon)

    clock = pygame.time.Clock()

    # Font used for small text in the hardware. Bigger text is usually image files.
    small_font = pygame.font.Font(script_dir + '/resources/fonts/5Pts5.ttf', 10)

    # Default hardware state when the hardware first starts.
    game_state = 'title'
    running = True
    file_handler = FileHandler()

    # A group of all the sprites on screen. Used to update all sprites at onc
    all_sprites = pygame.sprite.Group()

    # Start the GPIO handler to take in buttons from the RPi HAT.
    GPIOHandler.setup()

    # Dev code used to exit the hardware. Default Down, Down, Up, Up, Down, Down, Up, Up, A, A, B
    dev_code = deque()
    for button in [Constants.buttons.get('j_d'), Constants.buttons.get('j_d'), Constants.buttons.get('j_u'),
                   Constants.buttons.get('j_u'), Constants.buttons.get('j_d'), Constants.buttons.get('j_d'),
                   Constants.buttons.get('j_u'), Constants.buttons.get('j_u'), Constants.buttons.get('a'),
                   Constants.buttons.get('a'), Constants.buttons.get('b')]:
        dev_code.append(button)

    # Log of the inputs.
    input_log = deque()

    # Time since last input. Used to help regulate double presses of buttons.
    last_input_tick = 0

    def draw():
        """
        Draws the main pygame display.
        """

        # Draws all the sprites on screen and scales the screen to the correct size from the rendered size.
        all_sprites.update()
        all_sprites.draw(surface)
        frame = pygame.transform.scale(surface, (screen_size, screen_size))
        window.blit(frame, frame.get_rect())

        # Update the entire display.
        pygame.display.flip()

    def draw_bg():
        """
        Draws the main hardware background image onto a given surface.
        """
        bg_image = pygame.image.load(script_dir + '/resources/images/bg.png').convert()
        surface.blit(bg_image, (0, 0))

    def log_button(pressed_button):
        """
        Logs the button presses to register the dev code.
        :param pressed_button: The button code to be logged
        """
        input_log.append(pressed_button)
        if len(input_log) > len(dev_code):
            input_log.popleft()

    def create_event(pressed_button):
        """
        Creates a pygame event with a given keyboard code
        :param pressed_button:
        """
        nonlocal last_input_tick
        # Register a button click so long as the last button click happened no less than two frames ago
        if pygame.time.get_ticks() - last_input_tick > clock.get_time() * 2:
            pygame.event.post(pygame.event.Event(KEYDOWN, {'key': pressed_button}))
            pygame.event.post(pygame.event.Event(KEYUP, {'key': pressed_button}))
            log_button(pressed_button)
        last_input_tick = pygame.time.get_ticks()

    def check_dev_code():
        """
        Checks if the dev code has been entered. If it has, stop the program.
        """
        nonlocal running

        if dev_code == input_log:
            running = False

    def handle_gpio():
        """
        Handles getting GPIO button presses and making a pygame event when a press is detected.
        """
        for pressed_button in Constants.buttons:
            code = Constants.buttons.get(pressed_button)

            # Check if a button has been pressed. If it has, create a pygame event for it.
            if GPIOHandler.get_press(code):
                create_event(code)

    def keyboard_handler():
        """
        Simulates key presses to GPIO button presses. Also handles quitting the hardware.
        """
        nonlocal running

        # Checks if a corresponding keyboard key has been pressed. If it has, emulate a button press.
        for keyboard_event in pygame.event.get():
            if keyboard_event.type == pygame.QUIT:
                running = False
            if keyboard_event.type == pygame.KEYDOWN:
                if keyboard_event.key == pygame.K_a:
                    create_event(Constants.buttons.get('a'))
                if keyboard_event.key == pygame.K_b:
                    create_event(Constants.buttons.get('b'))
                if keyboard_event.key == pygame.K_PERIOD:
                    create_event(Constants.buttons.get('j_i'))
                if keyboard_event.key == pygame.K_RIGHT:
                    create_event(Constants.buttons.get('j_r'))
                if keyboard_event.key == pygame.K_LEFT:
                    create_event(Constants.buttons.get('j_l'))
                if keyboard_event.key == pygame.K_DOWN:
                    create_event(Constants.buttons.get('j_d'))
                if keyboard_event.key == pygame.K_UP:
                    create_event(Constants.buttons.get('j_u'))
                if keyboard_event.key == pygame.K_ESCAPE:
                    running = False

    def pre_handler():
        """
        Runs at the beginning of each loop, handles drawing the background, controlling hardware speed, and
        controlling the GPIO button inputs and keyboard handler
        """
        # Regulate the speed of the hardware.
        clock.tick(game_fps)

        # Handle all inputs for both debugging and real GPIO button presses.
        keyboard_handler()
        handle_gpio()
        check_dev_code()

        # Draw the background.
        draw_bg()

    while running:
        if game_state == 'title':
            all_sprites.empty()
            pre_handler()

            # Draw the title image in the middle of the screen.
            title_image = pygame.image.load(script_dir + '/resources/images/title.png').convert_alpha()
            surface.blit(title_image, (0, 0))
            draw()

            # Show the title for 1 second then move on to the initialization phase of the hardware.
            pygame.time.wait(1000)
            game_state = 'init'

        elif game_state == 'playground':
            all_sprites.empty()
            game_state = None  # Playground currently not implemented, send to error screen.

        elif game_state == 'init':
            all_sprites.empty()
            pre_handler()
            draw()

            # Read the save file.
            file_handler.read_save()

            # Determines if it is a new hardware or not by looking at the evolution stage. If it is -1, the egg has
            # not been created yet, and the hardware sends you to the egg selection screen. If not, the hardware sends
            # you to the playground.
            if file_handler.attributes['evolution_stage'] == -1:
                game_state = 'egg_select'
            else:
                game_state = 'playground'

        elif game_state == 'egg_select':

            # Submenu used within the egg selection menu.
            submenu = 'main'

            selected = 0

            while running and game_state == 'egg_select':
                all_sprites.empty()
                if submenu == 'main':

                    # Creates and holds the egg objects in a list.
                    eggs = [SelectionEgg('red'), SelectionEgg('orange'), SelectionEgg('yellow'),
                            SelectionEgg('green'),
                            SelectionEgg('blue'), SelectionEgg('indigo'), SelectionEgg('violet'), SelectionEgg('white'),
                            SelectionEgg('rainbow')]

                    # How many eggs per row should be displayed.
                    eggs_per_row = 3
                    distance_between_eggs = 36 / eggs_per_row

                    # Count the total rows.
                    total_rows = -(-len(eggs) // eggs_per_row)
                    distance_between_rows = 32 / eggs_per_row

                    # Determine the location of each egg.
                    for egg in eggs:
                        current_row = eggs.index(egg) // eggs_per_row
                        rows_after = total_rows - (current_row + 1)
                        egg_in_row = eggs.index(egg) % eggs_per_row
                        eggs_after = min(len(eggs) - (current_row * eggs_per_row), eggs_per_row) - (egg_in_row + 1)

                        x_offset = 32
                        y_offset = 30

                        # The x coordinate of an egg is determined by which egg in the row it is, and how many eggs
                        # are in that row. If there is only 1 egg in a row, it is in the middle of the screen. If
                        # there are two, they're on equal halves and so on.
                        x = x_offset - (eggs_after * distance_between_eggs) + (egg_in_row * distance_between_eggs)
                        y = y_offset - (rows_after * distance_between_rows) + (current_row * distance_between_rows)

                        egg.rect.x = x
                        egg.rect.y = y

                        # Add the egg to the sprite list.
                        all_sprites.add(egg)
                    selected = 0

                    def get_cursor_coords(selection):
                        """
                        Gets the coordinates of an egg on the selection screen by index and returns it as a tuple
                        :param selection: index of the egg to be selected
                        :return: tuple of the coordinates of the selected egg
                        """
                        cursor_x_offset = -2
                        cursor_y_offset = -2

                        return eggs[selection].rect.x + cursor_x_offset, eggs[selection].rect.y + cursor_y_offset

                    def sel_left():
                        """
                        Select the egg to the left with constraints.
                        """
                        nonlocal selected

                        if selected % eggs_per_row != 0:
                            selected -= 1

                    def sel_right():
                        """
                        Select the egg to the right with constraints.
                        """
                        nonlocal selected

                        row = selected // eggs_per_row
                        eggs_in_row = min(len(eggs) - (row * eggs_per_row), eggs_per_row)

                        if selected % eggs_per_row != eggs_in_row - 1:
                            selected += 1

                    def sel_up():
                        """
                        Select the egg above with constraints.
                        """
                        nonlocal selected

                        if selected // eggs_per_row != 0:
                            selected -= eggs_per_row

                    def sel_down():
                        """
                        Select the egg below with constraints.
                        """
                        nonlocal selected

                        if selected // eggs_per_row != total_rows - 1:
                            selected += eggs_per_row

                    while running and game_state == 'egg_select' and submenu == 'main':

                        pre_handler()

                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                if event.key == Constants.buttons.get('j_r'):
                                    sel_right()
                                if event.key == Constants.buttons.get('j_l'):
                                    sel_left()
                                if event.key == Constants.buttons.get('j_d'):
                                    sel_down()
                                if event.key == Constants.buttons.get('j_u'):
                                    sel_up()
                                if event.key == Constants.buttons.get('a'):
                                    # Advance to the egg info screen for the selected egg.
                                    submenu = 'egg_info'

                        # Draws the cursor on screen.
                        cursor = pygame.image.load(script_dir + '/resources/images/clock_selector.png').convert_alpha()
                        surface.blit(cursor, get_cursor_coords(selected))

                        draw()

                elif submenu == 'egg_info':
                    while running and game_state == 'egg_select' and submenu == 'egg_info':
                        pre_handler()
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                if event.key == Constants.buttons.get('a'):
                                    # Go to an invalid hardware state if continuing.
                                    game_state = None
                                if event.key == Constants.buttons.get('b'):
                                    # Go back to the egg selection screen.
                                    submenu = 'main'

                        # Quick debugging for which egg is selected.
                        selection_debug = small_font.render('Egg {0}'.format(selected), False, (64, 64, 64))
                        surface.blit(selection_debug, (5, 35))

                        draw()

                else:  # Go to the error state if an invalid state is set.
                    game_state = None

        else:
            # Error screen. This appears when an invalid hardware state has been selected.

            all_sprites.empty()
            frames_passed = 0  # Counter for frames, helps ensure the hardware isnt frozen.

            while running and game_state != 'title':

                pre_handler()

                # Draw the error screen
                error_screen = pygame.image.load(script_dir + '/resources/images/debug/invalid.png').convert_alpha()
                surface.blit(error_screen, (0, -8))

                # Counts the frames passed. Resets every second.
                frames_passed += 1
                if frames_passed >= game_fps:
                    frames_passed = 0

                # Draws the frame counter.
                frame_counter = small_font.render('frames: {0}'.format(frames_passed), False, (64, 64, 64))
                surface.blit(frame_counter, (1, 70))

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == Constants.buttons.get('b'):
                            # Reset back to the title screen.
                            game_state = 'title'

                draw()


def main():
    """
    Calls the hardware() function to start the hardware.
    """
    game()

    GPIOHandler.teardown()
    pygame.quit()