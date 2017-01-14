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
import unittest
from xdcc_dl.logging.Logger import Logger
from xdcc_dl.logging.LoggingTypes import LoggingTypes


class UnitTests(unittest.TestCase):

    def setUp(self):
        self.logfile = os.path.join(os.getcwd(), "logging_log")
        self.messages = [("Invisible", LoggingTypes.INVISIBLE),
                         ("Default", LoggingTypes.DEFAULT),
                         ("WHOIS_SEND", LoggingTypes.WHOIS_SEND),
                         ("PRIVATE_NOTICE", LoggingTypes.PRIVATE_NOTICE),
                         ("MESSAGE_OF_THE_DAY", LoggingTypes.MESSAGE_OF_THE_DAY),
                         ("EVENT", LoggingTypes.EVENT),
                         ("CHANNEL_KICK", LoggingTypes.CHANNEL_KICK)]

    def tearDown(self):
        if os.path.isfile(self.logfile):
            os.remove(self.logfile)

    def test_verbosity(self, ignore_verbosity=False):

        for verbosity_level in range(0, 7):

            logger = Logger(verbosity_level, self.logfile, ignore_verbosity)

            for message in self.messages:
                logger.log(message[0], message[1])

            with open(self.logfile, 'r') as l:
                log = l.read().rstrip().lstrip()

            if ignore_verbosity:
                self.assertEqual(len(log.split("\n")), 7)
            else:
                self.assertEqual(len(log.split("\n")), verbosity_level + 1)

            os.remove(self.logfile)

    def test_ignore_verbosity(self):
        self.test_verbosity(True)

    def test_logger_with_existing_logfile(self):

        with open(self.logfile, 'w') as f:
            f.write("Testing Logger\n")

        logger = Logger(1, self.logfile)
        logger.log("Test")

        with open(self.logfile, 'r') as f:
            self.assertEqual(f.read(), "Testing Logger\nTest\n")
