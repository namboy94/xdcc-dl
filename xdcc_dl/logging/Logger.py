import logging
from colorama import Fore, Back, Style


# noinspection PyMethodMayBeStatic
class Logger(object):
    """
    Class that handles log and print calls in the bot
    """

    logging_level = logging.WARNING
    """
    The logging level to display
    """

    def log(self, message: str, level: int, back: Back = Back.BLACK,
            fore: Fore = Fore.GREEN, end: str = "\n"):
        """
        Logs a message at the specified logging level
        :param message: The message to log
        :param level: The level at which to log the message
        :param back: The background color to print
        :param fore: The foreground color to print
        :param end: Characters to append to the string (Default newline)
        :return: None
        """
        if self.logging_level <= level:
            print(fore + back + message + Style.RESET_ALL + end)

    def info(self, message: str, back: Back = Back.BLACK,
             fore: Fore = Fore.GREEN, end: str = "\n"):
        """
        Logs a message at the INFO level
        :param message: The message to log
        :param back: The background color to print
        :param fore: The foreground color to print
        :param end: Characters to append to the string (Default newline)
        :return: None
        """
        self.log(message, logging.INFO, back, fore, end)

    def debug(self, message: str, back: Back = Back.WHITE,
              fore: Fore = Fore.BLACK, end: str = "\n"):
        """
        Logs a message at the DEBUG level
        :param message: The message to log
        :param back: The background color to print
        :param fore: The foreground color to print
        :param end: Characters to append to the string (Default newline)
        :return: None
        """
        self.log(message, logging.DEBUG, back, fore, end)

    def error(self, message: str, back: Back = Back.RED,
              fore: Fore = Fore.BLUE, end: str = "\n"):
        """
        Logs a message at the ERROR level
        :param message: The message to log
        :param back: The background color to print
        :param fore: The foreground color to print
        :param end: Characters to append to the string (Default newline)
        :return: None
        """
        self.log(message, logging.ERROR, back, fore, end)

    def warning(self, message: str, back: Back = Back.YELLOW,
                fore: Fore = Fore.BLUE, end: str = "\n"):
        """
        Logs a message at the WARNING level
        :param message: The message to log
        :param back: The background color to print
        :param fore: The foreground color to print
        :param end: Characters to append to the string (Default newline)
        :return: None
        """
        self.log(message, logging.WARNING, back, fore, end)
