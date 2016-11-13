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
import unittest
from xdcc_dl.pack_searchers.PackSearcher import PackSearcher


class UnitTests(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_all_searchers(self):

        results = PackSearcher().search("Gin.txt")
        self.assertEqual(len(results), 4)

    def test_getting_searchers(self):

        procedures = PackSearcher.get_available_pack_searchers()
        searcher = PackSearcher()

        for procedure in procedures:
            self.assertTrue(PackSearcher.procedure_map[procedure] in searcher.procedures)

    def test_selected_searchers(self):

        searcher = PackSearcher(["nibl", "namibsun"])
        self.assertEqual(len(searcher.search("Gin.txt")), 1)

        for procedure in PackSearcher.get_available_pack_searchers():

            if procedure not in ["nibl", "namibsun"]:
                self.assertFalse(PackSearcher.procedure_map[procedure] in searcher.procedures)
