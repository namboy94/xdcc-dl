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
import struct
import irc.client
# noinspection PyPep8Naming
from xdcc_dl.logging.LoggingTypes import LoggingTypes as LOG
from xdcc_dl.xdcc.layers.xdcc.XDCCInitiator import XDCCInitiator


class AlreadyDownloaded(Exception):
    """
    Gets thrown if a file already exists with size >= download size
    """
    pass


# noinspection PyUnusedLocal
class DownloadHandler(XDCCInitiator):
    """
    Class that handles the download process
    Layer 5 of the XDCC Bot
    """

    def on_dccmsg(self, connection: irc.client.ServerConnection, event: irc.client.Event) -> None:
        """
        Runs each time a new chunk of data is received while downloading

        :param connection: the IRC Connection
        :param event:      the IRC Event
        :return:           None
        """
        if self.already_downloaded:  # Send a single message to the server indicating that the transfer is done
            self.dcc_connection.send_bytes(struct.pack(b"!I", self.progress.get_single_progress_total()))

        else:

            data = event.arguments[0]
            data_length = len(data)

            self.file.write(data)
            self.progress.add_single_progress(data_length)

            progress_message = " Progress: %.2f" % self.progress.get_single_progress_percentage()
            progress_message += "% (" + str(self.progress.get_single_progress())
            progress_message += "/" + str(self.progress.get_single_progress_total()) + ")"

            self.logger.log(progress_message, LOG.DOWNLOAD_PROGRESS, carriage_return=True)

            # Send Acknowledge Message
            self.dcc_connection.send_bytes(struct.pack(b"!I", self.progress.get_single_progress()))
            # -> on_dccmsg if download not yet complete
            # -> on_dcc_disconnect if completed

    def on_dcc_disconnect(self, connection: irc.client.ServerConnection, event: irc.client.Event) -> None:
        """
        The DCC Connection was disconnected. Checks if download was completed. If not, try to resend Pack request

        :param connection: the IRC Connection
        :param event:      the IRC Event
        :return:           None
        """
        if self.file is not None:
            self.file.close()

            if os.path.getsize(self.current_pack.get_filepath()) < self.filesize:
                self.logger.log("Download Incomplete, Trying again.", LOG.DOWNLOAD_INCOMPLETE)
                self.connection.privmsg(self.current_pack.get_bot(), self.current_pack.get_request_message())
                return
            else:
                self.logger.log("\nDownload completed in %.2f seconds" % (time.time() - self.start_time), LOG.DEFAULT)

        if len(self.pack_queue) > 0:

            if not self.current_pack.get_server().get_address() == self.pack_queue[0].get_server().get_address():
                self.quit()  # -> on_disconnect

            else:
                self.pack_states[self.current_pack] = "OK"
                self.reset_connection_state()
                self.connected_to_server = True
                self.current_pack = self.pack_queue.pop(0)
                self.progress.next_file()
                self.connection.whois(self.current_pack.get_bot())

        else:
            self.quit()  # -> on_disconnect

    def on_disconnect(self, connection: irc.client.ServerConnection, event: irc.client.Event) -> None:
        """
        Extends the disconnect method by adding a check for already downloaded files

        :param connection: the IRC Connection
        :param event:      the IRC Event
        :return:           None
        """
        if self.already_downloaded:
            raise AlreadyDownloaded()
        else:
            super().on_disconnect(connection, event)
