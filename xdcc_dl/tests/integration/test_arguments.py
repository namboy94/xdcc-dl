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
import sys
import unittest
from xdcc_dl.main import main


class UnitTests(unittest.TestCase):

    def setUp(self):
        sys.argv = [sys.argv[0]]

    def tearDown(self):
        sys.argv = [sys.argv[0]]

    def test_no_arguments(self):
        try:
            main()
            self.assertEqual(True, False)
        except SystemExit:
            self.assertEqual(True, True)

    def test_keyboard_interrupt(self):

        if sys.version_info[0] >= 3:
            exec("import builtins as __builtin__") in globals()

            # noinspection PyUnusedLocal
            def interrupt(arg):
                if arg == "No arguments passed. See --help for more details":
                    raise KeyboardInterrupt()
                else:
                    self.assertEqual("Thanks for using xdcc-downloader!", arg)

            exec("real_print = __builtin__.print") in globals()
            exec("__builtin__.print = interrupt") in globals()

            main()

            exec("__builtin__.print = real_print") in globals()
