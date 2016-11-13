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
import time
import urwid
from threading import Thread
from xdcc_dl.metadata import General
from xdcc_dl.entities.Progress import Progress
from xdcc_dl.pack_searchers.PackSearcher import PackSearcher
from xdcc_dl.entities.XDCCPack import xdcc_packs_from_xdcc_message
from xdcc_dl.xdcc.MultipleServerDownloader import MultipleServerDownloader


# noinspection PyUnusedLocal
class XDCCDownloaderTui(object):
    """
    Class that models a urwid TUI for the XDCC Downloader
    """

    def __init__(self) -> None:
        """
        Initializes the TUI's various widgets
        """
        self.upper_body = []
        self.upper_middle_body = []
        self.middle_body = []
        self.lower_middle_body = []
        self.lower_body = []

        self.loop = None
        self.top = None
        self.list_walker = None

        self.downloading = False
        self.searching = False

        self.downloader = None

        self.search_results = []
        self.search_results_checks = []
        self.download_queue = []
        self.download_queue_checks = []

        self.gpl_notice = urwid.Text("XDCC Downloader V " + General.version_number + "\n"
                                     "Copyright (C) 2016 Hermann Krumrey\n\n"
                                     "This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.\n"
                                     "This is free software, and you are welcome to redistribute it\n"
                                     "under certain conditions; type `show c' for details.")
        self.message_edit = urwid.Edit(caption="XDCC Message: ", edit_text="")
        self.server_edit = urwid.Edit(caption="Server: ", edit_text="irc.rizon.net")
        self.add_pack_button = urwid.Button("Add Pack")

        self.search_engine_label = urwid.Text("Search Engines")
        self.search_engine_options = []
        for search_engine in ["All"] + PackSearcher.get_available_pack_searchers():
            urwid.RadioButton(self.search_engine_options, search_engine)

        self.search_term_edit = urwid.Edit(caption="Search Term: ", edit_text="")
        self.search_button = urwid.Button("Search")
        self.search_results_label = urwid.Text("Search Results:")
        self.add_search_result_button = urwid.Button("Add Selected Packs")

        self.download_queue_label = urwid.Text("Download_Queue")
        self.remove_pack_button = urwid.Button("Remove Selected Packs")

        self.destination_edit = urwid.Edit(caption="Destination Directory: ", edit_text=os.getcwd())
        self.download_button = urwid.Button("Download")
        self.single_progress_bar = urwid.ProgressBar("Progress", "Total")
        self.total_progress_bar = urwid.ProgressBar("Progress", "Total")

        self.connect_widgets()
        self.lay_out()

    def connect_widgets(self) -> None:
        """
        Connects actions to the relevant widgets

        :return: None
        """
        urwid.connect_signal(self.add_pack_button, 'click', self.add_pack_manually)
        urwid.connect_signal(self.search_button, 'click', self.search)
        urwid.connect_signal(self.add_search_result_button, 'click', self.add_selected_search_result_packs)
        urwid.connect_signal(self.remove_pack_button, 'click', self.remove_selected_packs)
        urwid.connect_signal(self.download_button, 'click', self.download)

    def lay_out(self) -> None:
        """
        Handles the layout of the TUI elements

        :return: None
        """
        div = urwid.Divider()

        self.upper_body = [self.gpl_notice, div, self.message_edit, self.server_edit, self.add_pack_button, div,
                           self.search_engine_label] + self.search_engine_options +\
                          [div, self.search_term_edit, self.search_button, div, self.search_results_label]
        self.upper_middle_body = []
        self.middle_body = [self.add_search_result_button, div, self.download_queue_label]
        self.lower_middle_body = []
        self.lower_body = [self.remove_pack_button, div, self.destination_edit, self.download_button, div,
                           self.single_progress_bar, self.total_progress_bar]

        body = self.upper_body + self.upper_middle_body + self.middle_body + self.lower_middle_body + self.lower_body

        self.list_walker = urwid.SimpleFocusListWalker(body)
        self.top = urwid.Overlay(urwid.Padding(urwid.ListBox(self.list_walker), left=2, right=2),
                                 urwid.SolidFill(u'\N{MEDIUM SHADE}'),
                                 align='center', width=('relative', 80),
                                 valign='middle', height=('relative', 70),
                                 min_width=20, min_height=10)

    def start(self) -> None:  # pragma: no cover
        """
        Starts the TUI

        :return: None
        """
        self.loop = urwid.MainLoop(self.top, palette=[('reversed', 'standout', '')])

        try:
            self.loop.run()
        except Exception as e:
            if self.downloader is not None:
                self.downloader.quit()
            raise e

    def refresh_ui(self) -> None:
        """
        Refreshed the UI

        :return: None
        """
        self.download_queue_checks = []
        self.search_results_checks = []

        for result in self.search_results:
            self.search_results_checks.append(urwid.CheckBox(result.get_filename()))
        for item in self.download_queue:
            self.download_queue_checks.append(urwid.CheckBox(item.get_request_message(full=True)))

        self.upper_middle_body = self.search_results_checks
        self.lower_middle_body = self.download_queue_checks

        body = self.upper_body + self.upper_middle_body + self.middle_body + self.lower_middle_body + self.lower_body

        self.list_walker[:] = body
        self.loop.draw_screen()

    def add_pack_manually(self, button: urwid.Button) -> None:
        """
        Adds a manually defined XDCC pack to the download queue

        :param button: The Button that called this method
        :return:       None
        """
        message = self.message_edit.get_edit_text()
        server = self.server_edit.get_edit_text()
        self.download_queue += xdcc_packs_from_xdcc_message(message, server=server)
        self.refresh_ui()

    def add_selected_search_result_packs(self, button: urwid.Button) -> None:
        """
        Adds all selected packs in the search results to the download queue

        :param button: The Button that called this method
        :return:       None
        """
        for index, result in enumerate(self.search_results_checks):
            if result.get_state():
                self.download_queue.append(self.search_results[index])
        self.refresh_ui()

    def remove_selected_packs(self, button: urwid.Button) -> None:
        """
        Removes all selected packs from the download queue

        :param button: The Button that called this method
        :return:       None
        """
        pop_indexes = []
        for index, pack in enumerate(self.download_queue_checks):
            if pack.get_state():
                pop_indexes.append(index)

        for index in reversed(sorted(pop_indexes)):
            self.download_queue.pop(index)

        self.refresh_ui()

    def search(self, button: urwid.Button) -> None:
        """
        Starts searching with the configured options

        :param button: The Button that called this method
        :return:       None
        """
        if not self.searching:

            self.searching = True

            search_engine = list(filter(lambda x: x.get_state(), self.search_engine_options))[0].get_label()
            searcher = PackSearcher() if search_engine == "All" else PackSearcher([search_engine])
            search_term = self.search_term_edit.get_edit_text()

            def do_search():
                self.spin_buttons(search=True)
                self.search_results = searcher.search(search_term)
                self.refresh_ui()
                self.searching = False

            Thread(target=do_search).start()

    def download(self, button: urwid.Button) -> None:
        """
        Starts downloading all packs that are currently in the download queue

        :param button: The Button that called this method
        :return:       None
        """
        if not self.downloading:
            self.downloading = True

            destination = self.destination_edit.get_edit_text()
            if not os.path.isdir(destination):
                self.downloading = False
                self.show_message_popup("The entered directory does not exist.")
                return

            for pack in self.download_queue:
                pack.set_directory(destination)

            def do_download():

                progress = Progress(len(self.download_queue),
                                    callback=lambda a, b, single_percentage, d, e, total_percentage, g, h:
                                    self.update_progress(single_percentage, total_percentage))

                self.spin_buttons(download=True)
                self.downloader = MultipleServerDownloader("random")
                self.downloader.download(self.download_queue, progress)
                self.download_queue = []
                self.update_progress(0.0, 0.0)
                self.refresh_ui()
                self.downloader.quit()
                self.downloading = False

            Thread(target=do_download).start()

    def update_progress(self, single_precentage: float, total_percentage: float) -> None:
        """
        Updates the progress bars

        :param single_precentage: The single completion so far
        :param total_percentage:  The total completion so far
        :return:                  None
        """
        self.single_progress_bar.set_completion(single_precentage)
        self.total_progress_bar.set_completion(total_percentage)
        self.loop.draw_screen()

    def spin_buttons(self, download: bool = False, search: bool = False) -> None:
        """
        Starts the button spin animations

        :param download: If set, starts the spin animation for the download button
        :param search:   If set, starts the spin animation for the search button
        :return:         None
        """

        def spin_thread():

            while self.downloading or self.searching:

                if self.downloading and download:
                    new_text = "Downloading" + (self.download_button.get_label().count(".") % 3 + 1) * "."
                    self.download_button.set_label(new_text)

                if self.searching and search:
                    new_text = "Searching" + (self.search_button.get_label().count(".") % 3 + 1) * "."
                    self.search_button.set_label(new_text)

                self.loop.draw_screen()
                time.sleep(0.3)

            if download:
                self.download_button.set_label("Download")
            if search:
                self.search_button.set_label("Search")
            self.loop.draw_screen()

        Thread(target=spin_thread).start()

    def show_message_popup(self, message: str) -> None:
        """
        Method that shows a message popup dialog while hiding the TUI

        :param message: The message to display
        :return:        None
        """

        text = urwid.Text(message)
        button = urwid.Button("OK")
        urwid.connect_signal(button, 'click', lambda x: self.refresh_ui())  # pragma: no cover

        self.list_walker[:] = [text, button]
        self.loop.draw_screen()
