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
from threading import Thread
from xdcc_dl.entities.Progress import Progress
from xdcc_dl.pack_searchers.PackSearcher import PackSearcher
from xdcc_dl.entities.XDCCPack import xdcc_packs_from_xdcc_message
from xdcc_dl.gui.pyuic.xdcc_downloader import Ui_XDCCDownloaderWindow
from xdcc_dl.xdcc.MultipleServerDownloader import MultipleServerDownloader
from PyQt5.QtWidgets import QMainWindow, QApplication, QTreeWidgetItem, QPushButton, QMessageBox
from PyQt5.QtCore import pyqtSignal, Qt


class XDCCDownloaderGui(QMainWindow, Ui_XDCCDownloaderWindow):
    """
    Class that models a QT GUI for the XDCC Downloader
    """

    spinner_start_signal = pyqtSignal(str, name="spinner_start")
    spinner_updater_signal = pyqtSignal(QPushButton, str, name="spinner_updater")
    refresh_search_results_signal = pyqtSignal(str, name="refresh_search_results")
    refresh_download_queue_signal = pyqtSignal(str, name="refresh_download_queue")
    show_download_complete_message_signal = pyqtSignal(str, name="show_download_complete_message")
    progress_update_signal = pyqtSignal(float, float, name="progress_update")

    def __init__(self, parent: QMainWindow = None) -> None:
        """
        Sets up the interactive UI elements

        :param parent: the parent window
        """
        super().__init__(parent)
        self.setupUi(self)

        header = self.search_result_tree_widget.header()
        header.hideSection(header.logicalIndex(header.visualIndex(0)))

        self.spinner_start_signal.connect(lambda x: self.start_spinner(x))
        self.spinner_updater_signal.connect(lambda x, y: self.update_spinner(x, y))
        self.refresh_search_results_signal.connect(self.refresh_search_results)
        self.refresh_download_queue_signal.connect(self.refresh_download_queue)
        self.show_download_complete_message_signal.connect(self.show_download_complete_message)
        self.progress_update_signal.connect(self.progress_update)

        self.searching = False
        self.downloading = False
        self.downloader = None

        self.search_results = []
        self.download_queue = []

        for searcher in ["All"] + PackSearcher.get_available_pack_searchers():
            self.search_engine_combo_box.addItem(searcher)
        self.destination_edit.setText(os.getcwd())

        self.search_button.clicked.connect(self.search)
        self.download_button.clicked.connect(self.download)
        self.add_button.clicked.connect(self.add_pack)

        self.search_term_edit.returnPressed.connect(self.search)

        self.up_arrow_button.clicked.connect(lambda: self.move_packs(up=True))
        self.down_arrow_button.clicked.connect(lambda: self.move_packs(down=True))
        self.left_arrow_button.clicked.connect(self.remove_packs_from_queue)
        self.rigth_arrow_button.clicked.connect(self.add_packs_to_queue)

    def add_pack(self):

        message = self.message_edit.text()
        server = self.server_edit.text()

        self.download_queue += xdcc_packs_from_xdcc_message(message, server=server)
        self.refresh_download_queue()

    def search(self) -> None:
        """
        Starts the XDCC search

        :return: None
        """
        if not self.searching:

            self.searching = True

            search_term = self.search_term_edit.text()
            search_engine = self.search_engine_combo_box.currentText()
            search_engines = [search_engine] if search_engine != "All" else PackSearcher.get_available_pack_searchers()

            searcher = PackSearcher(search_engines)

            def search_thread():

                self.spinner_start_signal.emit("search")
                self.search_results = searcher.search(search_term)
                self.refresh_search_results_signal.emit("")
                self.searching = False

            Thread(target=search_thread).start()

    def refresh_search_results(self) -> None:
        """
        Refreshes the Search Results Tree Widget with the current search results

        :return: None
        """
        self.search_result_tree_widget.clear()
        self.search_results.sort(key=lambda x: x.get_bot())

        for i, result in enumerate(self.search_results):
            column = [str(i),
                      result.get_bot(), str(result.get_packnumber()), str(result.get_size()), result.get_filename()]
            self.search_result_tree_widget.addTopLevelItem(QTreeWidgetItem(column))

        self.search_result_tree_widget.sortByColumn(1, Qt.AscendingOrder)

    def start_spinner(self, spinner_type: str) -> None:
        """
        Starts a spinner animation while either searching or downloading

        :param spinner_type: The type of spinner (a string that's either 'download' or 'search')
        :return:         None
        """
        def spin():

            search = spinner_type == "search"
            download = spinner_type == "download"

            while self.searching or self.downloading:

                if self.searching and search:
                    new_text = "Searching" + (self.search_button.text().count(".") % 3 + 1) * "."
                    self.spinner_updater_signal.emit(self.search_button, new_text)

                if self.downloading and download:
                    new_text = "Downloading" + (self.download_button.text().count(".") % 3 + 1) * "."
                    self.spinner_updater_signal.emit(self.download_button, new_text)

                time.sleep(0.3)

            if search and not self.searching:
                self.search_button.setText("Search")
            if download and not self.downloading:
                self.download_button.setText("Download")

        Thread(target=spin).start()

    # noinspection PyMethodMayBeStatic
    def update_spinner(self, widget: QPushButton, text: str) -> None:
        """
        Sets the text of the given spinner button

        :param widget: The button to change the text of
        :param text:   The text to display
        :return:       None
        """
        widget.setText(text)

    def add_packs_to_queue(self):
        """
        Adds selected packs from the search results tree widget to the download queue

        :return: None
        """

        for item in self.search_result_tree_widget.selectedItems():
            self.download_queue.append(self.search_results[int(item.text(0))])

        self.refresh_download_queue()

    def remove_packs_from_queue(self) -> None:
        """
        Removes all selected elements from the Download Queue

        :return: None
        """
        rows_to_pop = []
        for row in self.download_queue_list_widget.selectedIndexes():
            rows_to_pop.append(row.row())

        for row in reversed(sorted(rows_to_pop)):
            self.download_queue.pop(row)

        self.refresh_download_queue()

    def move_packs(self, up: bool = False, down: bool = False) -> None:
        """
        Moves items on the queue up or down

        :param up:   Pushes the selected elements up
        :param down: Pushes the selected elements down
        :return:     None
        """

        size_check = (lambda x: x > 0) if up and not down else (lambda x: x < len(self.download_queue) - 1)
        index_change = (lambda x: x - 1) if up and not down else (lambda x: x + 1)

        indexes = self.download_queue_list_widget.selectedIndexes() if up and not down \
            else reversed(self.download_queue_list_widget.selectedIndexes())

        for row in indexes:

            index = row.row()
            if size_check(index):
                self.download_queue.insert(index_change(index), self.download_queue.pop(index))

        self.refresh_download_queue()

    def refresh_download_queue(self):
        """
        Reloads all elements currently in the download queue

        :return: None
        """
        self.download_queue_list_widget.clear()
        for pack in self.download_queue:
            self.download_queue_list_widget.addItem(pack.get_request_message(full=True))

    def download(self):
        """
        Starts the download of all packs in the download queue

        :return: None
        """
        if not self.downloading:

            directory = self.destination_edit.text()

            if not os.path.isdir(directory):

                msg = self.generate_message(QMessageBox.Warning, "Invalid Directory",
                                            "The entered directory is not valid", directory)

                if not sys.argv == [sys.argv[0], "-platform", "minimal"]:  # pragma: no cover
                    msg.exec_()

            else:

                self.downloading = True

                for pack in self.download_queue:
                    pack.set_directory(directory)

                def do_download():

                    progress = Progress(len(self.download_queue),
                                        callback=lambda a, b, sin, d, e, tot, g, h: self.progress_update_signal.emit(
                                            sin, tot))

                    self.spinner_start_signal.emit("download")
                    self.downloader = MultipleServerDownloader("random")
                    results = self.downloader.download(self.download_queue, progress)
                    self.download_queue = []
                    self.refresh_download_queue_signal.emit("")
                    self.progress_update_signal.emit(0.0, 0.0)
                    self.downloader.quit()
                    self.downloading = False

                    list_of_downloaded_packs = ""
                    for result in results:
                        list_of_downloaded_packs += result.get_filepath() + "\n"

                    self.show_download_complete_message_signal.emit(list_of_downloaded_packs)

                Thread(target=do_download).start()

    def progress_update(self, single_percentage: float, total_percentage: float):
        """
        Updates the progress bars

        :param single_percentage: The single completion percentage
        :param total_percentage:  The total completion percentage
        :return:                  None
        """
        self.single_progress_bar.setValue(single_percentage)
        self.total_progress_bar.setValue(total_percentage)

    # noinspection PyMethodMayBeStatic
    def generate_message(self, icon: int, title: str, text: str, detailed_text: str) -> QMessageBox:
        """
        Generates a Message Dialog

        :param icon:           The icon to display
        :param title:          The title to display
        :param text:           The primary text to display
        :param detailed_text:  The detailed text to display
        :return:               The generated message dialog
        """
        msg = QMessageBox()
        msg.setIcon(icon)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setInformativeText(detailed_text)
        msg.setStandardButtons(QMessageBox.Ok)
        return msg

    def show_download_complete_message(self, details: str) -> None:
        """
        Message shown when the download has finished

        :param details: A formatted list of packs
        :return:        None
        """
        msg = self.generate_message(QMessageBox.Information, "Download Complete",
                                    "The download has been completed", "List of downloaded packs:")
        msg.setDetailedText(details.rstrip().lstrip())

        if not sys.argv == [sys.argv[0], "-platform", "minimal"]:  # pragma: no cover
            msg.exec_()


def start():  # pragma: no cover
    """
    Starts the Start Page GUI

    :return: None
    """
    app = QApplication(sys.argv)
    form = XDCCDownloaderGui()
    form.show()
    app.exec_()
    form.searching = False
    form.downloading = False
    if form.downloader is not None:
        form.downloader.quit()
