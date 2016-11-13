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
import urwid
import unittest
from xdcc_dl.tui.XDCCDownloaderTui import XDCCDownloaderTui


class LoopDummy(object):
    def draw_screen(self):
        pass


# noinspection PyTypeChecker
class UnitTests(unittest.TestCase):

    def setUp(self):
        self.tui = XDCCDownloaderTui()
        self.tui.loop = LoopDummy()

    def tearDown(self):
        pass

    def test_adding_pack(self):
        self.assertEqual(len(self.tui.download_queue), 0)
        self.tui.message_edit.set_edit_text("/msg xdcc_servbot xdcc send #1")
        self.tui.server_edit.set_edit_text("irc.namibsun.net")
        self.tui.add_pack_manually(None)
        self.assertEqual(len(self.tui.download_queue), 1)

    def test_searching(self):
        self.assertEqual(len(self.tui.search_results), 0)
        self.tui.search_term_edit.set_edit_text("1_test.txt")
        self.select_search_engine("namibsun")
        self.tui.search(None)

        while self.tui.searching:
            pass

        self.assertEqual(len(self.tui.search_results), 1)

    def test_searching_while_searching(self):
        self.assertEqual(len(self.tui.search_results), 0)
        self.tui.search_term_edit.set_edit_text("one punch man")
        self.select_search_engine("nibl")
        self.tui.search(None)

        self.tui.search_term_edit.set_edit_text("1_test.txt")
        self.select_search_engine("namibsun")
        self.tui.search(None)

        while self.tui.searching:
            pass

        self.assertLess(10, len(self.tui.search_results))
        for pack in self.tui.search_results:
            self.assertNotEqual("1_test.txt", pack.get_filename())

    def test_adding_search_results_to_queue(self):
        self.test_searching()

        self.assertEqual(0, len(self.tui.download_queue))
        self.tui.add_selected_search_result_packs(None)
        self.tui.search_results_checks[0].set_state(True)
        self.assertEqual(0, len(self.tui.download_queue))
        self.tui.add_selected_search_result_packs(None)
        self.assertEqual(1, len(self.tui.download_queue))

    def select_search_engine(self, option):
        for engine in self.tui.search_engine_options:
            if engine.get_label() == option:
                engine.set_state(True)
            else:
                engine.set_state(False)