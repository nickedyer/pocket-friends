"""
Menu class to help with drawing menus on screen
"""


class Menu:
    """
    Menu class. Creates a menu with text to display and options
    """

    def __init__(self, menu_text=''):
        self._menu_text = menu_text
        self._options = []
        self._selection = 0

    def add_option(self, option):
        """
        Adds an option to the menu. Only allows instances of Menu.Option
        :param option:
        """
        if not isinstance(option, Menu.Option):
            raise TypeError('option must be an instance of Menu.Option')
        else:
            self._options.append(option)

    def get_option(self, index):
        """
        Gets an option object given the index of the option. Raises IndexError if given
        index is out of bounds.
        :param index: the index of the option
        :return: the option object
        """
        try:
            return self._options[index]
        except IndexError as ex:
            raise IndexError('option index out of range') from ex

    def select_next(self):
        """
        Selects the next option in the list. Wraps around to the first option if
        the last option is currently selected.
        """
        self._selection += 1
        if self._selection >= len(self._options):
            self._selection = 0

    def select_prev(self):
        """
        Selects the previous option in the list. Wraps around to the last option if
        the first option is currently selected.
        """
        self._selection -= 1
        if self._selection < 0:
            if len(self._options) > 0:
                self._selection = len(self._options) - 1
            else:
                self._selection = 0

    def run_selection(self, *args, **kwargs):
        """
        Runs the function that the currently selected option object points to.
        :param args: arguments to be passed to the function
        :param kwargs: keyword arguments to be passed to the function
        """
        try:
            return self._options[self._selection].run(*args, **kwargs)
        except IndexError as ex:
            raise Exception('menu has no options, cannot run a non-existent option') from ex

    def draw_menu(self):
        """
        Draws the menu on screen with a leading 20 blank lines.
        """
        print('\n' * 20)

        print(self._menu_text + '\n')

        for option in self._options:
            selection_char = '>'

            if self._options.index(option) != self._selection:
                selection_char = ' '

            print('{0} {1}'.format(selection_char, option.get_text()))

    class Option:
        """
        Class that defines options for the Menu class.
        """

        def __init__(self, option_text='', function=None, *args, **kwargs):
            self._option_text = option_text
            self._function = function
            self._default_args = args
            self._default_kwargs = kwargs

        def get_text(self):
            """
            Returns the text to be displayed by the option
            :return: the option text
            """
            return self._option_text

        def run(self, *args, **kwargs):
            """
            Runs the function that the option object points to. Returns None if
            there is no function or the given function is not valid.
            :param args: arguments to be passed to the function
            :param kwargs: keyword arguments to be passed to the function
            :return: the return value of the function (if any)
            """
            if len(args) == 0:
                args = self._default_args
            if len(kwargs) == 0:
                kwargs = self._default_kwargs

            try:
                return self._function(*args, **kwargs)
            except TypeError:
                return None
