"""
Module that helps with the handling of taking inputs from the GPIO pins on the Raspberry
Pi and converting them to events to be used in other places (pygame, etc.)
"""
import importlib.util

try:
    importlib.util.find_spec('RPi.GPIO')
    import RPi.GPIO as GPIO
except ImportError:
    import data.development.FakeGPIO as GPIO


class Constants:
    """
    Contains the constants used by the HAT to read in buttons
    """
    buttons = {
        'a': 31,  # A button
        'b': 29,  # B button
        'j_i': 7,  # Joystick in
        'j_u': 11,  # Joystick up
        'j_d': 15,  # Joystick down
        'j_l': 13,  # Joystick left
        'j_r': 16  # Joystick right
    }


class GPIOHandler:
    """
    Class to handle the GPIO inputs from the buttons.
    """

    @staticmethod
    def setup():
        """
        Primes the GPIO pins for reading the inputs of the buttons.
        """
        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(Constants.buttons.get('a'), GPIO.IN)
        GPIO.setup(Constants.buttons.get('b'), GPIO.IN)
        GPIO.setup(Constants.buttons.get('j_i'), GPIO.IN)
        GPIO.setup(Constants.buttons.get('j_u'), GPIO.IN)
        GPIO.setup(Constants.buttons.get('j_d'), GPIO.IN)
        GPIO.setup(Constants.buttons.get('j_l'), GPIO.IN)
        GPIO.setup(Constants.buttons.get('j_r'), GPIO.IN)

        GPIO.add_event_detect(Constants.buttons.get('a'), GPIO.FALLING)
        GPIO.add_event_detect(Constants.buttons.get('b'), GPIO.FALLING)
        GPIO.add_event_detect(Constants.buttons.get('j_i'), GPIO.FALLING)
        GPIO.add_event_detect(Constants.buttons.get('j_u'), GPIO.FALLING)
        GPIO.add_event_detect(Constants.buttons.get('j_d'), GPIO.FALLING)
        GPIO.add_event_detect(Constants.buttons.get('j_l'), GPIO.FALLING)
        GPIO.add_event_detect(Constants.buttons.get('j_r'), GPIO.FALLING)

    @staticmethod
    def teardown():
        """
        Cleans up the GPIO handler.
        """
        GPIO.cleanup()

    @staticmethod
    def get_press(button):
        """
        Returns true if a button has moved from not pressed to pressed.
        :param button: button to be detected
        :return: True if the button is has been pressed, False otherwise
        """
        return GPIO.event_detected(button)
