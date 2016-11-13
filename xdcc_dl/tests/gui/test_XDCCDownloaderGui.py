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
try:
    from PyQt5.QtCore import Qt
    from PyQt5.QtTest import QTest
    from xdcc_dl.gui.XDCCDownloaderGui import XDCCDownloaderGui, QApplication
except ImportError:
    Qt = QTest = XDCCDownloaderGui = QApplication = None

import os
import sys
import time
import unittest
from xdcc_dl.entities.XDCCPack import XDCCPack
from xdcc_dl.entities.IrcServer import IrcServer


class UnitTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        if QApplication is None or sys.version_info[0] < 3:
            raise unittest.SkipTest("Skipping on python 2 or import error")

        sys.argv = [sys.argv[0], "-platform", "minimal"]
        cls.app = QApplication(sys.argv)

    def setUp(self):
        sys.argv = [sys.argv[0], "-platform", "minimal"]
        self.form = XDCCDownloaderGui()

    def tearDown(self):
        self.form.downloading = False
        self.form.searching = False
        self.form.destroy()
        if os.path.isfile("1_test.txt"):
            os.remove("1_test.txt")
        if os.path.isfile("2_test.txt"):
            os.remove("2_test.txt")
        if os.path.isfile("3_test.txt"):
            os.remove("3_test.txt")

    def test_default_values(self):
        self.assertEqual(os.getcwd(), self.form.destination_edit.text())
        self.assertEqual("irc.rizon.net", self.form.server_edit.text())

    def test_searching(self):
        self.form.search_term_edit.setText("1_test.txt")
        self.assertEqual(self.form.search_term_edit.text(), "1_test.txt")
        self.form.search_engine_combo_box.setCurrentText("namibsun")
        self.assertEqual(self.form.search_engine_combo_box.currentText(), "namibsun")
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

    def test_download_packs(self):
        self.form.download_queue = [XDCCPack(IrcServer("irc.namibsun.net"), "xdcc_servbot", 1),
                                    XDCCPack(IrcServer("irc.namibsun.net"), "xdcc_servbot", 2),
                                    XDCCPack(IrcServer("irc.namibsun.net"), "xdcc_servbot", 3)]
        self.form.refresh_download_queue()

        self.assertEqual(self.form.destination_edit.text(), os.getcwd())
        QTest.mouseClick(self.form.download_button, Qt.LeftButton)

        while self.form.downloading:
            pass

        self.assertTrue(os.path.isfile("1_test.txt"))
        self.assertTrue(os.path.isfile("2_test.txt"))
        self.assertTrue(os.path.isfile("3_test.txt"))
        self.form.show_download_complete_message_signal.emit("")

    def test_download_while_downloading(self):
        self.form.download_queue = [XDCCPack(IrcServer("irc.namibsun.net"), "xdcc_servbot", 1),
                                    XDCCPack(IrcServer("irc.namibsun.net"), "xdcc_servbot", 3)]
        self.form.refresh_download_queue()
        QTest.mouseClick(self.form.download_button, Qt.LeftButton)

        time.sleep(0.5)

        self.form.download_queue = [XDCCPack(IrcServer("irc.namibsun.net"), "xdcc_servbot", 2)]
        self.form.refresh_download_queue()
        QTest.mouseClick(self.form.download_button, Qt.LeftButton)

        while self.form.downloading:
            pass

        self.assertTrue(os.path.isfile("1_test.txt"))
        self.assertFalse(os.path.isfile("2_test.txt"))
        self.assertTrue(os.path.isfile("3_test.txt"))
        self.form.show_download_complete_message_signal.emit("")

    def test_search_while_searching(self):

        self.form.search_term_edit.setText("1_test.txt")
        self.assertEqual(self.form.search_term_edit.text(), "1_test.txt")
        self.form.search_engine_combo_box.setCurrentText("All")
        self.assertEqual(self.form.search_engine_combo_box.currentText(), "All")

        QTest.mouseClick(self.form.search_button, Qt.LeftButton)

        self.form.search_term_edit.setText("2_test.txt")
        self.assertEqual(self.form.search_term_edit.text(), "2_test.txt")
        self.form.search_engine_combo_box.setCurrentText("namibsun")
        self.assertEqual(self.form.search_engine_combo_box.currentText(), "namibsun")

        QTest.mouseClick(self.form.search_button, Qt.LeftButton)

        while self.form.searching:
            pass

        self.form.refresh_search_results()
        self.form.search_result_tree_widget.selectAll()

        self.assertEqual(1, len(self.form.search_results))
        self.assertEqual(self.form.search_results[0].get_bot(), "xdcc_servbot")
        self.assertEqual(1, self.form.search_result_tree_widget.invisibleRootItem().childCount())

    def test_spinner(self):
        self.form.downloading = True
        self.form.spinner_start_signal.emit("download")
        self.form.searching = True
        self.form.spinner_start_signal.emit("search")
        time.sleep(1)
        self.form.downloading = False
        self.form.searching = False
        time.sleep(1)

    def test_spin_update(self):
        self.assertEqual(self.form.download_button.text(), "Download")
        self.form.spinner_updater_signal.emit(self.form.download_button, "NotDownload")
        self.assertEqual(self.form.download_button.text(), "NotDownload")

    def test_invalid_download_directory(self):
        self.form.destination_edit.setText("")
        QTest.mouseClick(self.form.download_button, Qt.LeftButton)

    def test_move_selection_up_or_down(self):
        self.form.download_queue = [XDCCPack(IrcServer("irc.namibsun.net"), "xdcc_servbot", 1),
                                    XDCCPack(IrcServer("irc.namibsun.net"), "xdcc_servbot", 2),
                                    XDCCPack(IrcServer("irc.namibsun.net"), "xdcc_servbot", 3)]
        self.form.refresh_download_queue()

        self.form.download_queue_list_widget.selectAll()
        QTest.mouseClick(self.form.up_arrow_button, Qt.LeftButton)

        self.form.download_queue_list_widget.selectAll()
        QTest.mouseClick(self.form.down_arrow_button, Qt.LeftButton)

        self.assertEqual(self.form.download_queue_list_widget.count(), 3)

    def test_progress_update(self):
        self.assertEqual(self.form.single_progress_bar.value(), 0.0)
        self.assertEqual(self.form.total_progress_bar.value(), 0.0)
        self.form.progress_update_signal.emit(50.0, 75.0)
        self.assertEqual(self.form.single_progress_bar.value(), 50.0)
        self.assertEqual(self.form.total_progress_bar.value(), 75.0)

    def test_removing_queue_items(self):
        self.form.download_queue = [XDCCPack(IrcServer("irc.namibsun.net"), "xdcc_servbot", 1),
                                    XDCCPack(IrcServer("irc.namibsun.net"), "xdcc_servbot", 2),
                                    XDCCPack(IrcServer("irc.namibsun.net"), "xdcc_servbot", 3)]
        self.form.refresh_download_queue()
        self.form.download_queue_list_widget.selectAll()

        self.assertEqual(self.form.download_queue_list_widget.count(), 3)
        self.assertEqual(len(self.form.download_queue), 3)
        self.assertEqual(len(self.form.download_queue_list_widget.selectedIndexes()), 3)

        QTest.mouseClick(self.form.left_arrow_button, Qt.LeftButton)

        self.assertEqual(self.form.download_queue_list_widget.count(), 0)
        self.assertEqual(len(self.form.download_queue), 0)
        self.assertEqual(len(self.form.download_queue_list_widget.selectedIndexes()), 0)
