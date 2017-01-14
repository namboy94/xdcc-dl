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
import sys
import unittest
from xdcc_dl.main import main


class UnitTests(unittest.TestCase):

    def setUp(self):
        sys.argv = [sys.argv[0]]
        sys.argv.append("-v")
        sys.argv.append("0")
        sys.argv.append("-s")
        sys.argv.append("irc.namibsun.net")

    def tearDown(self):

        sys.argv = [sys.argv[0]]
        if os.path.isfile("1_test.txt"):
            os.remove("1_test.txt")
        if os.path.isfile("2_test.txt"):
            os.remove("2_test.txt")
        if os.path.isfile("3_test.txt"):
            os.remove("3_test.txt")

    def test_single_download(self):

        sys.argv.append("/msg xdcc_servbot xdcc send #1")
        main()

        self.check_content(1)

    def test_wrong_server(self):

        sys.argv.pop()
        sys.argv.pop()

        sys.argv.append("/msg xdcc_servbot xdcc send #1")
        self.assertFalse(os.path.isfile("1_test.txt"))

    def test_repeated_download(self):

        sys.argv.append("/msg xdcc_servbot xdcc send #2")

        with open("2_test.txt", 'w') as testtwo:
            testtwo.write("This is a Test File for XDCC File Transfers\n\n")
            testtwo.write("This is Pack 2")

        self.check_content(2)
        main()

        self.check_content(2)
        os.remove("2_test.txt")
        main()

        self.check_content(2)

    def test_resume(self):

        sys.argv.append("/msg xdcc_servbot xdcc send #3")

        with open("3_test.txt", 'w') as testthree:
            testthree.write("This is a Test File for XDCC File Transfers\n\nThis is Pack 3")

        self.check_content(3)

        with open("3_test.txt", 'rb') as testthree:
            binary = testthree.read()

        with open("3_test.txt", 'wb') as testthree:
            testthree.write(binary[0:int(len(binary) / 2)])

        main()
        self.check_content(3)

    def test_range_downloading(self):

        sys.argv.append("/msg xdcc_servbot xdcc send #1-3")
        main()

        self.check_content(1)
        self.check_content(2)
        self.check_content(3)

    def test_range_downloading_with_steps(self):

        sys.argv.append("/msg xdcc_servbot xdcc send #1-3,2")
        main()

        self.check_content(1)
        self.assertFalse(os.path.isfile("2_test.txt"))
        self.check_content(3)

    def check_content(self, number):

        self.assertTrue(os.path.isfile(str(number) + "_test.txt"))
        with open(str(number) + "_test.txt", 'r') as f:

            content = f.read()
            self.assertTrue("This is a Test File for XDCC File Transfers" in content)
            self.assertTrue("This is Pack " + str(number) in content)
