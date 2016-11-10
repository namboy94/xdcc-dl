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
from PyQt5.QtWidgets import QMainWindow, QApplication, QTreeWidgetItem


class XDCCDownloaderGui(QMainWindow, Ui_XDCCDownloaderWindow):
    """
    Class that models a QT GUI for the XDCC Downloader
    """

    def __init__(self, parent: QMainWindow = None) -> None:
        """
        Sets up the interactive UI elements

        :param parent: the parent window
        """
        super().__init__(parent)
        self.setupUi(self)

        self.searching = False
        self.downloading = False

        self.search_results = []

        for searcher in ["All"] + PackSearcher.get_available_pack_searchers():
            self.search_engine_combo_box.addItem(searcher)

        self.search_button.clicked.connect(self.search)
        self.download_button.clicked.connect(self.download)
        self.add_button.clicked.connect(self.add_pack)

        # UI Updaters
        self.search_button.windowTitleChanged.connect(self.refresh_search_results)
        self.search_button.customContextMenuRequested.connect(lambda: self.start_spinner(search=True))
        self.download_button.windowTitleChanged.connect(self.cleanup_download_queue)
        self.download_button.customContextMenuRequested.connect(lambda: self.start_spinner(download=True))

        self.up_arrow_button.clicked.connect(lambda: self.move(1))
        self.down_arrow_button.clicked.connect(lambda: self.move(-1))
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

                self.search_button.customContextMenuRequested.emit()
                self.search_results = searcher.search(search_term)
                self.search_button.windowTitleChanged.emit()
                self.searching = False

            Thread(target=search_thread).start()

    def refresh_search_results(self) -> None:
        """
        Refreshes the Search Results Tree Widget with the current search results

        :return: None
        """
        self.search_result_tree_widget.clear()
        for result in self.search_results:
            column = [result.get_bot(), str(result.get_pack_number()), result.get_size(), result.get_filename()]
            self.search_result_tree_widget.addTopLevelItem(QTreeWidgetItem(column))

    def start_spinner(self, search: bool = False, download: bool = False) -> None:
        """
        Starts a spinner animation while either searching or downloading

        :param search:   Starts the search spinner if set
        :param download: Starts the download spinner if set
        :return:         None
        """

        while self.searching or self.downloading:

            if self.searching and search:
                self.search_button.setText("Searching" + (self.search_button.text().count(".") % 3 + 1) * ".")

            if self.downloading and download:
                self.download_button.setText("Searching" + (self.download_button.text().count(".") % 3 + 1) * ".")

            time.sleep(0.3)


def start():
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