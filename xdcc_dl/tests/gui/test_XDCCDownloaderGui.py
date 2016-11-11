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
import sys
import unittest
from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest
from xdcc_dl.entities.XDCCPack import XDCCPack
from xdcc_dl.entities.IrcServer import IrcServer
from xdcc_dl.gui.XDCCDownloaderGui import XDCCDownloaderGui, QApplication


class ExtendedXDCCDownloaderGui(XDCCDownloaderGui):

    def __init__(self, parent=None):
        super().__init__(parent)


class UnitTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = QApplication(sys.argv)

    def setUp(self):
        self.form = ExtendedXDCCDownloaderGui()

    def tearDown(self):
        self.form.destroy()

    def test_default_values(self):
        self.assertEqual(os.getcwd(), self.form.destination_edit.text())
        self.assertEqual("irc.rizon.net", self.form.server_edit.text())

    def test_searching(self):
        self.form.search_term_edit.setText("1_test.txt")
        self.assertEqual(self.form.search_term_edit.text(), "1_test.txt")
        self.form.search_engine_combo_box.setCurrentText("namibsun")
        QTest.mouseClick(self.form.search_button, Qt.LeftButton)

        while self.form.searching:
            pass

        self.form.refresh_search_results()
        self.form.search_result_tree_widget.selectAll()

        self.assertEqual(1, len(self.form.search_results))
        self.assertEqual(self.form.search_results[0].get_bot(), "xdcc_servbot")
        self.assertEqual(1, self.form.search_result_tree_widget.invisibleRootItem().childCount())

    def test_adding_search_result(self):
        self.test_searching()

        QTest.mouseClick(self.form.rigth_arrow_button, Qt.LeftButton)
        self.assertEqual(1, len(self.form.download_queue))
        self.assertEqual(1, self.form.download_queue_list_widget.count())

    def test_removing_pack_from_queue(self):
        self.form.download_queue = [XDCCPack(IrcServer("irc.namibsun.net"), "xdcc_servbot", 1)]
        self.form.refresh_download_queue()
        self.assertEqual(1, self.form.download_queue_list_widget.count())

        self.form.download_queue_list_widget.selectAll()
        QTest.mouseClick(self.form.left_arrow_button, Qt.LeftButton)

        self.assertEqual(0, len(self.form.download_queue))
        self.assertEqual(0, self.form.download_queue_list_widget.count())

    def test_adding_manual_pack(self):
        self.form.message_edit.setText("/msg xdcc_servbot xdcc send #1")
        self.form.server_edit.setText("irc.namibsun.net")
        self.assertEqual(self.form.message_edit.text(), "/msg xdcc_servbot xdcc send #1")
        self.assertEqual(self.form.server_edit.text(), "irc.namibsun.net")

        QTest.mouseClick(self.form.add_button, Qt.LeftButton)
        self.form.refresh_download_queue()
        self.assertEqual(1, len(self.form.download_queue))
        self.assertEqual(1, self.form.download_queue_list_widget.count())
