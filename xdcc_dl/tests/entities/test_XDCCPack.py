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
import os
import unittest
from xdcc_dl.entities.IrcServer import IrcServer
from xdcc_dl.entities.XDCCPack import XDCCPack, xdcc_packs_from_xdcc_message


class UnitTests(unittest.TestCase):

    def setUp(self):
        self.pack = XDCCPack(IrcServer("irc.namibsun.net"), "xdcc_servbot", 1)

    def tearDown(self):
        pass

    def test_getters(self):

        self.assertEqual(self.pack.get_packnumber(), 1)
        self.assertEqual(self.pack.get_bot(), "xdcc_servbot")
        self.assertEqual(self.pack.get_filename(), "")
        self.assertEqual(self.pack.get_size(), 0)
        self.assertEqual(self.pack.get_server(), "irc.namibsun.net")
        self.assertEqual(self.pack.get_filepath(), os.getcwd())
        self.assertEqual(self.pack.get_request_message(), "/msg xdcc_servbot xdcc send #1")

    def test_setting_filename(self):

        self.pack.set_filename("test")
        self.assertEqual(self.pack.get_filename(), "test")
        self.assertEqual(self.pack.get_filepath(), os.path.join(os.getcwd(), "test"))

        self.pack.set_filename("something")
        self.assertEqual(self.pack.get_filename(), "test")
        self.assertEqual(self.pack.get_filepath(), os.path.join(os.getcwd(), "test"))

        self.pack.set_filename("something", override=True)
        self.assertEqual(self.pack.get_filename(), "something")
        self.assertEqual(self.pack.get_filepath(), os.path.join(os.getcwd(), "something"))

        self.pack.set_filename("something_else.txt", override=True)
        self.assertEqual(self.pack.get_filename(), "something.txt")
        self.assertEqual(self.pack.get_filepath(), os.path.join(os.getcwd(), "something.txt"))

        self.pack.set_directory(os.path.join(os.getcwd(), "test"))
        self.assertEqual(self.pack.get_filename(), "something.txt")
        self.assertEqual(self.pack.get_filepath(), os.path.join(os.getcwd(), "test", "something.txt"))

    def test_original_filename_check(self):

        self.assertTrue(self.pack.is_filename_valid("the_original"))
        self.assertTrue(self.pack.is_filename_valid("not_the_original"))
        self.pack.set_original_filename("the_original")
        self.assertTrue(self.pack.is_filename_valid("the_original"))
        self.assertFalse(self.pack.is_filename_valid("not_the_original"))

    def test_generating_from_xdcc_message_single(self):

        packs = xdcc_packs_from_xdcc_message("/msg xdcc_servbot xdcc send #1", "testdir", "irc.namibsun.net")
        self.assertEqual(len(packs), 1)
        pack = packs[0]

        self.assertEqual(pack.get_packnumber(), 1)
        self.assertEqual(pack.get_bot(), "xdcc_servbot")
        self.assertEqual(pack.get_server(), "irc.namibsun.net")
        self.assertEqual(pack.get_filepath(), "testdir")

    def test_generating_from_xdcc_message_range(self):

        packs = xdcc_packs_from_xdcc_message("/msg xdcc_servbot xdcc send #1-100")
        self.assertEqual(len(packs), 100)

        for i, pack in enumerate(packs):
            self.assertEqual(pack.get_packnumber(), i + 1)
            self.assertEqual(pack.get_server(), "irc.rizon.net")
            self.assertEqual(pack.get_filepath(), os.getcwd())

    def test_generating_from_xdcc_message_range_with_jumps(self):

        packs = xdcc_packs_from_xdcc_message("/msg xdcc_servbot xdcc send #1-100,2")
        self.assertEqual(len(packs), 50)

        i = 1
        for pack in packs:
            self.assertEqual(pack.get_packnumber(), i)
            i += 2
