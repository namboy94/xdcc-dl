"""
LICENSE:
Copyright 2015,2016 Hermann Krumrey

This file is part of toktokkie.

    toktokkie is a program that allows convenient managing of various
    local media collections, mostly focused on video.

    toktokkie is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    toktokkie is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with toktokkie.  If not, see <http://www.gnu.org/licenses/>.
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
            import builtins as __builtin__

            def interrupt(arg):
                if arg == "No arguments passed. See --help for more details":
                    raise KeyboardInterrupt()
                else:
                    self.assertEqual("Thanks for using xdcc-downloader!", arg)

            real_print = __builtin__.print
            __builtin__.print = interrupt

            main()

            __builtin__.print = real_print
