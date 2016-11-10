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

# imports
import os
from typing import Dict
from xdcc_dl.logging.LoggingTypes import LoggingTypes


class Logger(object):
    """
    Logger for IRC/XDCC related events with variable verbosity levels
    """

    def __init__(self, verbosity_level: int, logfile: str = None, ignore_verbosity_in_logfile: bool = True) -> None:
        """
        Initializes a new Logger object. The verbosity of the logger is defined here.
        Optionally, a logfile can be used to log to a file in addition to the console.
        If a logfile is specified, everything, regardless of verbosity level, will be logged
        to the file by default, but may be changed by toggling the ignore_verbosity_in_logfile parameter

        :param verbosity_level:             the verbosity level to be used. for more information, see
                                            xdcc_dl.logging.LoggingTypes
        :param logfile:                     The path to a logfile. Specifying this is optional
        :param ignore_verbosity_in_logfile: Determines if the logfile uses the same verbosity level settings
                                            as the console logging. By default, the verbosity setting is ignored
        """
        self.verbosity_level = verbosity_level
        self.logfile = logfile
        self.ignore_logfile_verbosity = ignore_verbosity_in_logfile

        if self.logfile is not None:
            if not os.path.isfile(self.logfile):
                open(self.logfile, 'w').close()

    def log(self, message: str, logging_type: Dict[str, str or int]=None, carriage_return: bool = False) -> None:
        """
        Logs a message to the console and optionally to a logfile

        :param message:         the message to log
        :param logging_type:    the type of message to log
        :param carriage_return: If set to true, appends a carriage return to the log message
        :return:                None
        """
        if logging_type is None:
            logging_type = LoggingTypes.DEFAULT

        priority = logging_type['priority']

        if self.logfile is not None:
            if self.ignore_logfile_verbosity or self.verbosity_level >= priority:
                with open(self.logfile, 'a') as log:
                    log.write(message + "\n")

        if self.verbosity_level >= priority:

            fg_color = logging_type["fg_color"]
            bg_color = logging_type["bg_color"]

            end = "\n" if not carriage_return else "\r"

            print(fg_color + bg_color + message + '\033[0m' + '\033[0m', end=end)
