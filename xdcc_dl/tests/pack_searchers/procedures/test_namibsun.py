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
from xdcc_dl.pack_searchers.procedures.namibsun import find_namibsun_packs


class UnitTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_empty_query(self):
        packs = find_namibsun_packs("")
        self.assertEqual(len(packs), 0)

    def test_gin_txt(self):
        packs = find_namibsun_packs("1_test.txt")
        self.assertEqual(len(packs), 1)

        pack = packs[0]
        self.assertEqual(pack.get_packnumber(), 1)
        self.assertEqual(pack.get_server().get_address(), "irc.namibsun.net")
        self.assertEqual(pack.get_filepath(), os.path.join(os.getcwd(), pack.get_filename()))
        self.assertEqual(pack.get_filename(), "1_test.txt")
        self.assertEqual(pack.get_bot(), "xdcc_servbot")

    def test_non_result_query(self):
        self.assertEqual(0, len(find_namibsun_packs("sdgyfdhkdashsahdqhdsadlsajdhsaohdsausahoashdsahdlahdsah")))
