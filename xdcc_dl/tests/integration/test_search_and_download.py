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
import unittest
from xdcc_dl.xdcc.XDCCDownloader import XDCCDownloader
from xdcc_dl.pack_searchers.PackSearcher import PackSearcher


class UnitTests(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_search_and_download_namibsun(self):

        searcher = PackSearcher(["namibsun"])
        packs = searcher.search("1_test.txt") + searcher.search("2_test.txt")

        XDCCDownloader(packs[0].get_server(), "random").download(packs)