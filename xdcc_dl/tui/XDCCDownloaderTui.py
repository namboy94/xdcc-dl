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
from xdcc_dl.xdcc.MultipleServerDownloader import MultipleServerDownloader


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

        self.search_results = []
        self.download_queue = []

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
        self.search_results_label = urwid.Text("Search Results:")

        self.download_queue_label = urwid.Text("Download_Queue")

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
        pass

    def lay_out(self) -> None:
        """
        Handles the layout of the TUI elements

        :return: None
        """
        div = urwid.Divider()

        self.upper_body = [self.gpl_notice, div, self.message_edit, self.server_edit, self.add_pack_button, div,
                           self.search_engine_label] + self.search_engine_options + [div, self.search_term_edit,
                                                                                     self.search_results_label]
        self.upper_middle_body = []
        self.middle_body = [div, self.download_queue_label, div]
        self.lower_middle_body = []
        self.lower_body = [div, self.download_button, div, self.single_progress_bar, self.total_progress_bar]

        body = self.upper_body + self.upper_middle_body + self.middle_body + self.lower_middle_body + self.lower_body

        self.list_walker = urwid.SimpleFocusListWalker(body)
        self.top = urwid.Overlay(urwid.Padding(urwid.ListBox(self.list_walker), left=2, right=2),
                                 urwid.SolidFill(u'\N{MEDIUM SHADE}'),
                                 align='center', width=('relative', 80),
                                 valign='middle', height=('relative', 70),
                                 min_width=20, min_height=10)

    def start(self) -> None:
        """
        Starts the TUI

        :return: None
        """
        self.loop = urwid.MainLoop(self.top, palette=[('reversed', 'standout', '')])
        self.loop.run()


