"""
Module to test the GPIO input on the Raspberry Pi.
"""
from collections import deque
from pocket_friends.hardware.gpio_handler import Constants, GPIOHandler


def button_test():
    """
    GPIO button test. Checks for a GPIO input and prints it out, simple as that.
    """
    running = True

    # Exit code used to quit the button test.
    exit_code = deque()
    for button in ['j_d', 'j_d', 'j_u', 'j_u', 'j_d', 'j_d', 'j_u', 'j_u', 'a', 'a', 'b']:
        exit_code.append(button)

    # Input log to check for quitting out of the button test.
    input_log = deque()

    GPIOHandler.setup()

    def log(pressed_button):
        """
        Logs the pressed button into the input log.
        :param pressed_button:
        """
        input_log.append(pressed_button)
        if len(input_log) > len(exit_code): # Don't let the input log exceed the length of the exit code.
            input_log.popleft()

    def check_exit():
        """
        Check if the input log and the exit code are the same. If they are, quit the button test.
        """
        nonlocal running

        if exit_code == input_log:
            running = False

    while running:
        for button in Constants.buttons:
            code = Constants.buttons.get(button)
            if GPIOHandler.get_press(code): # If a button is pressed, print it out and do a quit check.
                print('event: {0}'.format(button))
                log(button)
                check_exit()

    GPIOHandler.teardown()
