"""
Module used to fake the RPi.GPIO module so that
the hardware can be run without the actual hardware.
"""

# Constants used by RPi.GPIO
BOARD = 0
IN = 0
FALLING = 0


def setmode(new_mode):
    """
    Fake setmode function.
    :param new_mode:
    """
    pass


def setup(channel, mode, initial=None, pull_up_down=None):
    """
    Fake setup function.
    :param channel:
    :param mode:
    :param initial:
    :param pull_up_down:
    """
    pass


def add_event_detect(channel, edge_type, callback=None, bouncetime=0):
    """
    Fake function to add a non-existent event detect.
    :param channel:
    :param edge_type:
    :param callback:
    :param bouncetime:
    """
    pass


def event_detected(channel):
    """
    Fake function to detect an event. Always returns false.
    :param channel:
    :return:
    """
    return False


def cleanup(channel=None):
    """
    Fake cleanup function.
    :param channel:
    """
    pass
