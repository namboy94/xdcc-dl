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
from xdcc_dl.pack_searchers.procedures.ixirc import find_ixirc_packs


class UnitTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_empty_query(self):
        packs = find_ixirc_packs("")
        self.assertEqual(len(packs), 0)

    def test_gin_txt(self):
        packs = find_ixirc_packs("Gin.txt")
        self.assertEqual(len(packs), 1)

        pack = packs[0]
        self.assertEqual(pack.get_packnumber(), 1)
        self.assertEqual(pack.get_server().get_address(), "irc.abjects.net")
        self.assertEqual(pack.get_filepath(), os.path.join(os.getcwd(), pack.get_filename()))
        self.assertEqual(pack.get_filename(), "Gin.txt")
        self.assertEqual(pack.get_bot(), "Beast-Gin-Anime")

    def test_larger_result(self):
        packs = find_ixirc_packs("One Punch Man")
        self.assertLess(10, len(packs))

    def test_non_result_query(self):
        self.assertEqual(0, len(find_ixirc_packs("sdgyfdhkdashsahdqhdsadlsajdhsaohdsausahoashdsahdlahdsah")))

    def test_invalid_pack_handling(self):
        self.assertLess(10, len(find_ixirc_packs("Star Wars Episode 7")))
