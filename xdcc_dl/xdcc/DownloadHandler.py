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
import time
import struct
import irc.client
from typing import List
from xdcc_dl.entities.User import User
from xdcc_dl.logging.Logger import Logger
from xdcc_dl.entities.XDCCPack import XDCCPack
from xdcc_dl.entities.Progress import Progress
from xdcc_dl.xdcc.XDCCInitiator import XDCCInitiator
# noinspection PyPep8Naming
from xdcc_dl.logging.LoggingTypes import LoggingTypes as LOG


# noinspection PyUnusedLocal
class DownloadHandler(XDCCInitiator):
    """
    Class that handles the download process
    Layer 5 of the XDCC Bot
    """

    def __init__(self, packs: List[XDCCPack], user: User, logger: Logger, progress: Progress, print_pause: float = 1.0)\
            -> None:
        """
        Initializes the XDCC Initiator object. Defines local DCC connection and the opened download file

        :param packs:       the packs to download
        :param user:        the username to use
        :param logger:      the logger to use
        :param progress:    the Progress object to keep track of the download progress
        :param print_pause: the time amount between download progress prints
        """
        super().__init__(packs, user, logger, progress)
        self.print_pause = print_pause
        self.start_time = time.time()

    def on_dccmsg(self, connection: irc.client.ServerConnection, event: irc.client.Event) -> None:
        """
        Runs each time a new chunk of data is received while downloading

        :param connection: the IRC Connection
        :param event:      the IRC Event
        :return:           None
        """
        data = event.arguments[0]
        data_length = len(data)

        self.file.write(data)
        self.progress.add_single_progress(data_length)

        progress_message = " Progress: %.2f" % self.progress.get_single_progress_percentage()
        progress_message += "% (" + str(self.progress.get_single_progress())
        progress_message += "/" + str(self.progress.get_single_progress_total()) + ")"

        self.logger.log(progress_message, LOG.DOWNLOAD_PROGRESS, carriage_return=True)

        # Send Acknowledge Message
        self.dcc_connection.send_bytes(struct.pack("!I", self.progress.get_single_progress()))

    def on_dcc_disconnect(self, connection: irc.client.ServerConnection, event: irc.client.Event) -> None:
        """
        The DCC Connection was disconnected. Checks if download was completed. If not, try to resend Pack request

        :param connection: the IRC Connection
        :param event:      the IRC Event
        :return:           None
        """
        if self.file is not None:
            self.file.close()
            self.logger.log("\nDownload completed in %.2f seconds" % (time.time() - self.start_time))

        self.connection.close()
        self.connection.disconnect()


if __name__ == "__main__":

    from xdcc_dl.entities.IrcServer import IrcServer
    xpacks = [XDCCPack(IrcServer("irc.rizon.net"), "CR-HOLLAND|NEW", 8920, "/home/hermann/testing/")]
    DownloadHandler(xpacks, User("Heramann"), Logger(5), Progress(len(xpacks))).start()
