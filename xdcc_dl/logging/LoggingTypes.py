"""
LICENSE:
Copyright 2016 Hermann Krumrey

This file is part of xdcc_dl.

    xdcc_dl is a program that allows downloading files via hte XDCC
    protocol via file serving bots on IRC networks.

    xdcc_dl is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    xdcc_dl is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with xdcc_dl.  If not, see <http://www.gnu.org/licenses/>.
LICENSE
"""


class FGColors:
    """
    Foreground Colours for colouring console output
    """

    DEFAULT = '\033[39m'
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    LIGHT_GRAY = '\033[37m'
    DARK_GRAY = '\033[90m'
    LIGHT_RED = '\033[91m'
    LIGHT_GREEN = '\033[92m'
    LIGHT_YELLOW = '\033[93m'
    LIGHT_BLUE = '\033[94m'
    LIGHT_MAGENTA = '\033[95m'
    LIGHT_CYAN = '\033[96m'
    WHITE = '\033[97m'


class BGColors:
    """
    Background Colours for colouring console output
    """

    DEFAULT = '\033[49m'
    BLACK = '\033[40m'
    RED = '\033[41m'
    GREEN = '\033[42m'
    YELLOW = '\033[43m'
    BLUE = '\033[44m'
    MAGENTA = '\033[45m'
    CYAN = '\033[46m'
    LIGHT_GRAY = '\033[47m'
    DARK_GRAY = '\033[100m'
    LIGHT_RED = '\033[101m'
    LIGHT_GREEN = '\033[102m'
    LIGHT_YELLOW = '\033[103m'
    LIGHT_BLUE = '\033[104m'
    LIGHT_MAGENTA = '\033[105m'
    LIGHT_CYAN = '\033[106m'
    WHITE = '\033[107m'


class LoggingTypes:
    """
    The different logging types.

    Each logging type is assigned a background and foreground colour and a priority. The priority
    determines if the type of logging element is shown at all. In General, the logging levels mean:

        0: Must be shown under all circumstances except pure GUI output
        1: Will definitely be shown in a CLI environment
        2: Will generally be shown in a CLI environment
    """

    CONNECTION_ATTEMPT = {"bg_color": BGColors.DEFAULT, "fg_color": FGColors.WHITE, "priority": 2}
    CONNECTION_SUCCESS = {"bg_color": BGColors.GREEN,   "fg_color": FGColors.WHITE, "priority": 2}
    CONNECTION_FAILURE = {"bg_color": BGColors.RED,     "fg_color": FGColors.WHITE, "priority": 2}
