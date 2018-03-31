"""
Copyright 2016-2017 Hermann Krumrey

This file is part of xdcc-dl.

xdcc-dl is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

xdcc-dl is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with xdcc-dl.  If not, see <http://www.gnu.org/licenses/>.
"""

# imports
import os
import time
from typing import List, Dict
from xdcc_dl.entities.XDCCPack import XDCCPack
from xdcc_dl.entities.Progress import Progress
from xdcc_dl.entities.IrcServer import IrcServer
from xdcc_dl.entities.User import User
from xdcc_dl.logging.Logger import Logger
# noinspection PyPep8Naming
from xdcc_dl.logging.LoggingTypes import LoggingTypes as LOG
from xdcc_dl.xdcc.legacy.layers import NetworkError, Disconnect
from xdcc_dl.xdcc.legacy.layers import BotNotFoundException
from xdcc_dl.xdcc.legacy.layers import DownloadHandler,\
    AlreadyDownloaded, IncompleteDownload
from xdcc_dl.xdcc.legacy.layers import IncorrectFileSentException,\
    NoValidWhoisQueryException


class XDCCDownloader(DownloadHandler):
    """
    The XDCC Downloader that combines the capabilities of
    all XDCC Layers to offer a stable interface to download XDCC Packs
    """

    def __init__(self, server: IrcServer or str, user: User or str,
                 logger: Logger or int = 0, timeout_time: int = 10):
        """
        Adds a check for stuck downloads every second that aborts and retries
        after 30 seconds without response
        :param server: The server to use
        :param user: The user to log in with
        :param logger: The logger used to log stuff
        :param timeout_time: The time to wait for a stuck download before
                             retrying
        """
        super().__init__(server, user, logger)

        def stuck_check():
            if self.download_started:
                if time.time() - self.last_dcc_data_timestamp > timeout_time:
                    self.logger.log(
                        "Download Stuck, Trying again.",
                        LOG.DOWNLOAD_INCOMPLETE)
                    self.dcc_connection.disconnect()
                    # self.download_started = False
                    # self.joined_channels = []
                    # self.quit()

        # self.reactor.scheduler.execute_every(period=5, func=stuck_check)

    def download(self, packs: List[XDCCPack], progress: Progress = None)\
            -> Dict[XDCCPack, str]:
        """
        Downloads all XDCC packs specified. Optionally shares state with other
        threads using a Progress object.
        All packs need to connect to the same server

        :param packs:    The packs to download
        :param progress: Optional Progress object
        :return: Dictionary of packs mapped to status codes:
                   "OK":              Download was successful
                   "BOTNOTFOUND":     Bot was not found
                   "CHANNELJOINFAIL": Channel join failed, most likely due to
                                      missing whois information
                   "NETWORKERROR":    Download failed due to network error
                   "INCORRECT":       Sent file was not the correct file
                   "EXISTED":         File already existed and was
                                      completely downloaded
                   "OTHERSERVER":     If a pack was found that is hosted on a
                                      different server
        """
        self.progress = progress if progress is not None else \
            Progress(len(packs))
        self.pack_queue = packs
        self.pack_states = {}

        while len(self.pack_queue) > 0:

            self.current_pack = self.pack_queue.pop(0)

            if self.current_pack.get_server().get_address() != \
                    self.server.get_address():
                self.pack_states[self.current_pack] = "OTHERSERVER"
                continue

            status_code = "OK"

            try:
                self.start()
            except BotNotFoundException:
                status_code = "BOTNOTFOUND"
            except NoValidWhoisQueryException:
                status_code = "CHANNELJOINFAIL"
            except AlreadyDownloaded:
                status_code = "EXISTED"
            except IncorrectFileSentException:
                status_code = "INCORRECT"
            except NetworkError:
                status_code = "NETWORKERROR"
            except Disconnect:
                status_code = "DISCONNECTED"
            except IncompleteDownload:
                status_code = "INCOMPLETE"

            path = self.current_pack.get_filepath()
            if os.path.getsize(path) < self.filesize:
                status_code = "INCOMPLETE"

            self.pack_states[self.current_pack] = status_code

            if status_code == "INCOMPLETE":
                self.pack_queue.insert(0, self.current_pack)
                self.progress.reset_current_file_progress()
            else:
                self.progress.next_file()

            self.reset_connection_state()

        self.quit()

        return self.pack_states
