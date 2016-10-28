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
        sys.argv.append("2")
        pass

    def tearDown(self):
        pass

    def test_gin_txt(self):

        sys.argv.append("-m")
        sys.argv.append("/msg ginpachi-sensei xdcc send #1")
        main()
        time.sleep(1)

        self.assertTrue(os.path.isfile("Gin.txt"))
        total_size = os.path.getsize("Gin.txt")

        main()
        time.sleep(1)

        self.assertTrue(os.path.isfile("Gin.txt"))
        self.assertAlmostEqual(os.path.getsize("Gin.txt"), total_size)

        with open("Gin.txt", 'rb') as f:
            content = f.read()
        with open("Gin.txt", 'wb') as f:
            f.write(content[0:int(total_size/2)])

        main()

        self.assertTrue(os.path.isfile("Gin.txt"))
        self.assertAlmostEqual(os.path.getsize("Gin.txt"), total_size)
        os.remove("Gin.txt")

    def test_mashiro_txt_download(self):

        sys.argv.append("-m")
        sys.argv.append("/msg E-D|Mashiro xdcc send #1")
        main()
        time.sleep(1)

        self.assertTrue(os.path.isfile("mashiro.txt"))
        total_size = os.path.getsize("mashiro.txt")

        main()
        time.sleep(1)

        self.assertTrue(os.path.isfile("mashiro.txt"))
        self.assertAlmostEqual(os.path.getsize("mashiro.txt"), total_size)

        with open("mashiro.txt", 'rb') as f:
            content = f.read()
        with open("mashiro.txt", 'wb') as f:
            f.write(content[0:int(total_size / 2)])

        main()
        self.assertTrue(os.path.isfile("mashiro.txt"))
        self.assertAlmostEqual(os.path.getsize("mashiro.txt"), total_size)
        os.remove("mashiro.txt")
