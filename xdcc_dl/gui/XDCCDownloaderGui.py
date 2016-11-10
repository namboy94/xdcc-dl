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
import sys
import time
from threading import Thread
from xdcc_dl.pack_searchers.PackSearcher import PackSearcher
from xdcc_dl.gui.pyuic.xdcc_downloader import Ui_XDCCDownloaderWindow
from PyQt5.QtWidgets import QMainWindow, QApplication, QTreeWidgetItem, QPushButton
from PyQt5.QtCore import pyqtSignal, Qt



class XDCCDownloaderGui(QMainWindow, Ui_XDCCDownloaderWindow):  # pragma: no cover
    """
    Class that models a QT GUI for the XDCC Downloader
    """

    spinner_start_signal = pyqtSignal(str, name="spinner_start")
    spinner_updater_signal = pyqtSignal(QPushButton, str, name="spinner_updater")
    refresh_search_results_signal = pyqtSignal(str, name="refresh_search_results")

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

        self.searching = False
        self.downloading = False

        self.search_results = []
        self.download_queue = []

        for searcher in ["All"] + PackSearcher.get_available_pack_searchers():
            self.search_engine_combo_box.addItem(searcher)

        self.search_button.clicked.connect(self.search)
        self.download_button.clicked.connect(self.download)
        self.add_button.clicked.connect(self.add_pack)

        self.up_arrow_button.clicked.connect(lambda: self.move_pack(1))
        self.down_arrow_button.clicked.connect(lambda: self.move_pack(-1))
        self.left_arrow_button.clicked.connect(self.remove_packs)
        self.rigth_arrow_button.clicked.connect(self.add_packs)

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
                self.search_button.setText("Download")

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

    def add_packs(self):
        """
        Adds selected packs from the search results tree widget to the download queue

        :return: None
        """

        for item in self.search_result_tree_widget.selectedItems():
            print(item.text(4))
            self.download_queue.append(self.search_results[int(item[0])])

        self.refresh_download_queue()

    def remove_packs(self):
        """
        Removes the currently selected Packs from the download queue

        :return: None
        """

        for item in self.download_queue_list_widget.selectedIndexes():
            self.download_queue_list_widget.pop(item.row())

        self.refresh_download_queue()

    def add_to_queue(self) -> None:
        """
        Add the currently selected items in the search result list to the download queue

        :return: None
        """
        for index, row in enumerate(self.search_result_tree_widget.selectedIndexes()):
            if index % 5 != 0:
                continue

            self.search_result_tree_widget.selectedItems()

            self.download_queue_list.append(self.search_results[row.row()])
            self.refresh_download_queue()

        self.search_result_list.clearSelection()

    def remove_from_queue(self) -> None:
        """
        Removes all selected elements from the Download Queue

        :return: None
        """
        for row in reversed(self.download_queue_list_widget.selectedIndexes()):
            self.download_queue.pop(row.row())
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
        pass
    def cleanup_download_queue(self):
        pass
    def add_pack(self):
        pass
    def move_pack(self, direction: int):
        pass


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


if __name__ == '__main__':
    start()
