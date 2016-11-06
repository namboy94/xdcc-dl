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
import time
import unittest
from xdcc_dl.main import main


class UnitTests(unittest.TestCase):

    def setUp(self):
        sys.argv = [sys.argv[0]]
        sys.argv.append("-v")
        sys.argv.append("5")

    def tearDown(self):
        if os.path.isfile("Gin.txt"):
            os.remove("Gin.txt")
        if os.path.isfile("mashiro.txt"):
            os.remove("mashiro.txt")

    def test_gin_txt(self):

        sys.argv.append("-m")
        sys.argv.append("/msg ginpachi-sensei xdcc send #1")
        main()
        time.sleep(5)

        self.assertTrue(os.path.isfile("Gin.txt"))
        total_size = os.path.getsize("Gin.txt")

        main()
        time.sleep(5)

        self.assertTrue(os.path.isfile("Gin.txt"))
        self.almost_equal(os.path.getsize("Gin.txt"), total_size)

        with open("Gin.txt", 'rb') as f:
            content = f.read()
        with open("Gin.txt", 'wb') as f:
            f.write(content[0:int(total_size/2)])

        main()
        time.sleep(5)

        self.assertTrue(os.path.isfile("Gin.txt"))
        self.almost_equal(os.path.getsize("Gin.txt"), total_size)

    def test_mashiro_txt_download(self):

        sys.argv.append("-m")
        sys.argv.append("/msg E-D|Mashiro xdcc send #1")
        main()
        time.sleep(5)

        self.assertTrue(os.path.isfile("mashiro.txt"))
        total_size = os.path.getsize("mashiro.txt")

        main()
        time.sleep(5)

        self.assertTrue(os.path.isfile("mashiro.txt"))
        self.almost_equal(os.path.getsize("mashiro.txt"), total_size)

        with open("mashiro.txt", 'rb') as f:
            content = f.read()
        with open("mashiro.txt", 'wb') as f:
            f.write(content[0:int(total_size / 2)])

        main()
        time.sleep(5)

        self.assertTrue(os.path.isfile("mashiro.txt"))
        self.almost_equal(os.path.getsize("mashiro.txt"), total_size)

    def almost_equal(self, param_one, param_two):
        self.assertTrue(param_two - 15 <= param_one <= param_two + 15)
