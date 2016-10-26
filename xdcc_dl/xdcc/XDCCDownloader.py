"""
LICENSE:
Copyright 2016 Hermann Krumrey

This file is part of xdcc_dl.

    xdcc_dl is a program that allows downloading files via hte XDCC
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
from typing import List, Dict

from xdcc_dl.entities.XDCCPack import XDCCPack
from xdcc_dl.entities.Progress import Progress
from xdcc_dl.xdcc.layers.irc.BaseIrcClient import NetworkError
from xdcc_dl.xdcc.layers.irc.BotFinder import BotNotFoundException
from xdcc_dl.xdcc.layers.xdcc.XDCCInitiator import AlreadyDownloaded
from xdcc_dl.xdcc.layers.xdcc.DownloadHandler import DownloadHandler, IncompleteDownload


class XDCCDownloader(DownloadHandler):
    """
    The XDCC Downloader that combines the capabilities of all XDCC Layers to offer a stable
    interface to download XDCC Packs
    """

    def download(self, packs: List[XDCCPack], progress: Progress = None) -> Dict[XDCCPack, str]:
        """
        Downloads all XDCC packs specified. Optionally shares state with other threads using a Progress object

        :param packs:    The packs to download
        :param progress: Optional Progress object
        :return:         Dictionary of packs mapped to status codes:
                         "OK":           Download was successful
                         "BOTNOTFOUND":  Bot was not found
                         "NETWORKERROR": Download failed due to network error
                         "INCOMPLETE":   Download was incomplete
                         "EXISTED":      File already existed and was completely downloaded
        """
        self.progress = progress if progress is not None else Progress(len(packs))

        pack_states = {}
        for pack in packs:
            self.current_pack = pack

            status_code = "OK"

            try:
                print("starting")
                self.start()
            except BotNotFoundException:
                status_code = "BOTNOTFOUND"
            except IncompleteDownload:
                status_code = "INCOMPLETE"
            except AlreadyDownloaded:
                status_code = "EXISTED"
            except NetworkError:
                status_code = "NETWORKERROR"

            pack_states[self.current_pack] = status_code

        return pack_states
