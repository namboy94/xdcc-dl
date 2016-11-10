"""
LICENSE:
Copyright 2016 Hermann Krumrey

This file is part of xdcc_dl.

    xdcc_dl is a program that allows downloading files via the XDCC
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
    BLACK = '\033[40m'  # WHITE
    RED = '\033[41m'
    GREEN = '\033[42m'  # YELLOW
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
        3: Will be shown in environments where detailed output is desired
        4: Will generally not be shown, may lead to excessive amount of output
        5: Shows all undefined events. WILL lead to excessive output
        6: Has nothing to do with the task at hand

    Colour Coding:

        YELLOW/L_YELLOW BG:                    DCC / Downloads
        CYAN BG:                               WHOIS
        GREEN BG:                              CHANNELS
        BLUE BG:                               Messages
        DEFAULT BG + GREY/L_GREY/WHITE FG:     Welcome Messages, Message of the day, CTCP Version
        DEFAULT BG + DEFAULT/L_GREEN/L_RED FG: Connection
        DEFAULT BG + BLUE/L_BLUE FG:           Private Message/Notice
        DEFAULT BG + YELLOW/L_YELLOW FG:       Public Message/Notice
        DEFAULT BG + MANGENTA/L_MAGENTA FG:    Undefined events
    """

    INVISIBLE            = {"bg_color": BGColors.DEFAULT,      "fg_color": FGColors.DEFAULT,        "priority": 0}
    DEFAULT              = {"bg_color": BGColors.DEFAULT,      "fg_color": FGColors.DEFAULT,        "priority": 1}

    CONNECTION_ATTEMPT   = {"bg_color": BGColors.DEFAULT,      "fg_color": FGColors.DEFAULT,        "priority": 2}
    CONNECTION_SUCCESS   = {"bg_color": BGColors.DEFAULT,      "fg_color": FGColors.LIGHT_GREEN,    "priority": 2}
    CONNECTION_FAILURE   = {"bg_color": BGColors.DEFAULT,      "fg_color": FGColors.LIGHT_RED,      "priority": 2}
    BANNED               = {"bg_color": BGColors.LIGHT_RED,    "fg_color": FGColors.LIGHT_MAGENTA,  "priority": 1}

    WHOIS_SEND           = {"bg_color": BGColors.CYAN,         "fg_color": FGColors.BLACK,          "priority": 2}
    WHOIS_SUCCESS        = {"bg_color": BGColors.CYAN,         "fg_color": FGColors.WHITE,          "priority": 2}
    WHOIS_NO_RESULT      = {"bg_color": BGColors.CYAN,         "fg_color": FGColors.LIGHT_RED,      "priority": 2}
    WHOIS_USER           = {"bg_color": BGColors.CYAN,         "fg_color": FGColors.DARK_GRAY,      "priority": 4}
    WHOIS_SERVER         = {"bg_color": BGColors.CYAN,         "fg_color": FGColors.LIGHT_GRAY,     "priority": 4}

    CHANNEL_JOIN_ATTEMPT = {"bg_color": BGColors.GREEN,        "fg_color": FGColors.BLACK,          "priority": 2}
    CHANNEL_JOIN_SUCCESS = {"bg_color": BGColors.GREEN,        "fg_color": FGColors.LIGHT_GREEN,    "priority": 2}
    CHANNEL_USERS        = {"bg_color": BGColors.GREEN,        "fg_color": FGColors.LIGHT_BLUE,     "priority": 6}
    CHANNEL_TOPIC        = {"bg_color": BGColors.GREEN,        "fg_color": FGColors.MAGENTA,        "priority": 6}
    CHANNEL_QUIT         = {"bg_color": BGColors.GREEN,        "fg_color": FGColors.RED,            "priority": 6}
    CHANNEL_PART         = {"bg_color": BGColors.GREEN,        "fg_color": FGColors.LIGHT_MAGENTA,  "priority": 6}
    CHANNEL_KICK         = {"bg_color": BGColors.GREEN,        "fg_color": FGColors.LIGHT_RED,      "priority": 6}
    CHANNEL_MODE_CHANGE  = {"bg_color": BGColors.GREEN,        "fg_color": FGColors.LIGHT_YELLOW,   "priority": 6}
    CHANNEL_ACTION       = {"bg_color": BGColors.GREEN,        "fg_color": FGColors.YELLOW,         "priority": 6}
    CHANNEL_NICK_CHANGED = {"bg_color": BGColors.GREEN,        "fg_color": FGColors.LIGHT_CYAN,     "priority": 6}

    MESSAGE_SEND         = {"bg_color": BGColors.BLUE,          "fg_color": FGColors.BLACK,         "priority": 1}
    MESSAGE_RETRY        = {"bg_color": BGColors.BLUE,          "fg_color": FGColors.WHITE,         "priority": 1}

    ALREADY_REQUESTED    = {"bg_color": BGColors.BLUE,          "fg_color": FGColors.LIGHT_RED,     "priority": 2}

    INCORRECT_FILE       = {"bg_color": BGColors.YELLOW,        "fg_color": FGColors.LIGHT_MAGENTA, "priority": 1}
    DCC_SEND_HANDSHAKE   = {"bg_color": BGColors.YELLOW,        "fg_color": FGColors.BLACK,         "priority": 2}
    DCC_RESUME_REQUEST   = {"bg_color": BGColors.YELLOW,        "fg_color": FGColors.DARK_GRAY,     "priority": 2}
    DCC_RESUME_SUCCESS   = {"bg_color": BGColors.YELLOW,        "fg_color": FGColors.WHITE,         "priority": 2}
    DCC_RESUME_FAILED    = {"bg_color": BGColors.YELLOW,        "fg_color": FGColors.LIGHT_RED,     "priority": 2}

    DOWNLOAD_START       = {"bg_color": BGColors.LIGHT_YELLOW,  "fg_color": FGColors.LIGHT_GREEN,   "priority": 1}
    DOWNLOAD_RESUME      = {"bg_color": BGColors.LIGHT_YELLOW,  "fg_color": FGColors.LIGHT_BLUE,    "priority": 1}
    DOWNLOAD_PROGRESS    = {"bg_color": BGColors.LIGHT_YELLOW,  "fg_color": FGColors.BLACK,         "priority": 1}
    DOWNLOAD_WAS_DONE    = {"bg_color": BGColors.LIGHT_YELLOW,  "fg_color": FGColors.RED,           "priority": 1}
    DOWNLOAD_INCOMPLETE  = {"bg_color": BGColors.LIGHT_YELLOW,  "fg_color": FGColors.LIGHT_RED,     "priority": 2}

    PRIVATE_NOTICE       = {"bg_color": BGColors.DEFAULT,      "fg_color": FGColors.BLUE,           "priority": 3}
    PRIVATE_MESSAGE      = {"bg_color": BGColors.DEFAULT,      "fg_color": FGColors.LIGHT_BLUE,     "priority": 3}
    PUBLIC_NOTICE        = {"bg_color": BGColors.DEFAULT,      "fg_color": FGColors.YELLOW,         "priority": 4}
    PUBLIC_MESSAGE       = {"bg_color": BGColors.DEFAULT,      "fg_color": FGColors.LIGHT_YELLOW,   "priority": 4}

    MESSAGE_OF_THE_DAY   = {"bg_color": BGColors.DEFAULT,      "fg_color": FGColors.LIGHT_GRAY,     "priority": 4}
    WELCOME              = {"bg_color": BGColors.DEFAULT,      "fg_color": FGColors.DARK_GRAY,      "priority": 4}
    CTCP_VERSION         = {"bg_color": BGColors.DEFAULT,      "fg_color": FGColors.WHITE,          "priority": 4}
    PING                 = {"bg_color": BGColors.LIGHT_GREEN,  "fg_color": FGColors.BLACK,          "priority": 4}

    EVENT                = {"bg_color": BGColors.DEFAULT,      "fg_color": FGColors.MAGENTA,        "priority": 5}
    EVENT_TEXT           = {"bg_color": BGColors.DEFAULT,      "fg_color": FGColors.LIGHT_MAGENTA,  "priority": 5}
