"""
Copyright 2016-2018 Hermann Krumrey

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

import os
import time
import struct
import shlex
from xdcc_dl.entities.XDCCPack import XDCCPack
from xdcc_dl.entities.User import User
from xdcc_dl.xdcc.exceptions import InvalidCTCPException, \
    AlreadyDownloadedException, DownloadCompleted
from irc.client import SimpleIRCClient, ServerConnection, Event, \
    ip_numstr_to_quad


class XDCCCLient(SimpleIRCClient):
    """
    IRC Client that can download an XDCC pack
    """

    def __init__(self, pack: XDCCPack):
        """
        Initializes the XDCC IRC client
        :param pack: The pack to download
        """
        self.user = User()
        self.pack = pack
        self.server = pack.server
        self.downloading = False
        self.xdcc_timestamp = 0
        self.channels = None  # to list if channel joins are required
        self.message_sent = False

        # XDCC state variables
        self.peer_address = ""
        self.peer_port = -1
        self.filesize = -1
        self.progress = 0
        self.xdcc_file = None
        self.xdcc_connection = None

        super().__init__()

    def download(self) -> str:
        """
        Downloads the pack
        :return: The path to the downloaded file
        """
        try:
            self.connect(
                self.server.address,
                self.server.port,
                self.user.username
            )
            self.start()
        except AlreadyDownloadedException:
            pass
        except DownloadCompleted:
            pass
        finally:
            self.reactor.disconnect_all()
            return self.pack.get_filepath()

    def on_welcome(self, conn: ServerConnection, _: Event):
        """
        The 'welcome' event indicates a successful connection to the server
        Sends a whois command to find the bot on the server
        :param conn: The connection
        :param _: The 'welcome' event
        :return: None
        """
        print("Welcome")
        conn.whois(self.pack.bot)

    def on_whoischannels(self, conn: ServerConnection, event: Event):
        """
        The 'whoischannels' event indicates that a whois request has found
        channels that the bot is a part of.
        Channels that the bot has joined will be joined as well.
        :param conn: The connection
        :param event: The 'whoischannels' event
        :return: None
        """
        print("WHOIS Channels: " + str(event.arguments))
        channels = event.arguments[1].split("#")
        channels.pop(0)
        channels = list(map(lambda x: "#" + x.split(" ")[0], channels))
        self.channels = channels

        for channel in self.channels:
            # Join all channels to avoid only joining a members-only channel
            conn.join(channel)

    def on_endofwhois(self, conn: ServerConnection, _: Event):
        """
        The 'endofwhois' event indicates the end of a whois request.
        This manually calls on_join in case the bot
        has not joined any channels.
        :param conn: The connection
        :param _: The 'endofwhois' event
        :return: None
        """
        print("End of WHOIS")
        if self.channels is None:
            self.on_join(conn, _)

    def on_join(self, conn: ServerConnection, event: Event):
        """
        The 'join' event indicates that a channel was successfully joined.
        The first on_join call will send a message to the bot that requests
        the initialization of the XDCC file transfer.
        :param conn: The connection
        :param event: The 'join' event
        :return: None
        """
        # Make sure we were the ones joining
        if not event.source.startswith(self.user.get_name()):
            return
        print("Joined Channel: " + event.target)

        if not self.message_sent:
            print("Send MSG")
            self.message_sent = True
            conn.privmsg(self.pack.bot, self.pack.get_request_message())

    def on_ctcp(self, conn: ServerConnection, event: Event):
        """
        The 'ctcp' event indicates that a CTCP message was received.
        The downloader receives a CTCP from the bot to initialize the
        XDCC file transfer.
        Handles DCC ACCEPT and SEND messages. Other DCC messages will result
        in a raised InvalidCTCP exception.
        DCC ACCEPT will only occur when a resume request was sent successfully.
        DCC SEND will occur when the bot offers a file.
        :param conn: The connection
        :param event: The 'ctcp' event
        :return: None
        :raise InvalidCTCPException: In case no valid DCC message was received
        """

        print("Source: " + str(event.source))
        print("Args: " + str(event.arguments))
        print("Type: " + str(event.type))
        print("Tags: " + str(event.tags))
        print("Target: " + str(event.target))

        def start_download(append: bool = False):
            """
            Helper method that starts the download of an XDCC pack
            :param append: If set to True, opens the file in append mode
            :return: None
            """
            self.downloading = True
            self.xdcc_timestamp = time.time()
            mode = "ab" if append else "wb"
            print("Start Download: " + mode)
            self.xdcc_file = open(self.pack.get_filepath(), mode)
            self.xdcc_connection = \
                self.dcc_connect(self.peer_address, self.peer_port, "raw")

        print("CTCP: " + str(event.arguments))
        if event.arguments[0] == "DCC":
            payload = shlex.split(event.arguments[1])

            if payload[0] == "SEND":

                filename = payload[1]
                self.peer_address = ip_numstr_to_quad(payload[2])
                self.peer_port = int(payload[3])
                self.filesize = int(payload[4])

                self.pack.set_filename(filename)

                if os.path.isfile(self.pack.get_filepath()):

                    position = os.path.getsize(self.pack.get_filepath())

                    if position >= self.filesize:
                        raise AlreadyDownloadedException(self.pack.filename)

                    print("Resume")
                    self.progress = position
                    bot = event.source.split("!")[0]
                    resume_param = "\"" + filename + "\" " + \
                                   str(self.peer_port) + " " + str(position)
                    conn.ctcp("DCC RESUME", bot, resume_param)

                else:
                    start_download()

            elif payload[0] == "ACCEPT":
                start_download(append=True)

            else:
                raise InvalidCTCPException(payload[0])

    def on_dccmsg(self, _: ServerConnection, event: Event):
        """
        The 'dccmsg' event contains the file data.
        :param _: The connection
        :param event: The 'dccmsg' event
        :return: None
        """
        self.xdcc_timestamp = time.time()

        data = event.arguments[0]
        data_length = len(data)

        self.xdcc_file.write(data)
        self.progress += data_length

        self.xdcc_connection.send_bytes(struct.pack(b"!Q", self.progress))
        print("Progress: " + str(self.progress / self.filesize), end="\r")

    def on_dcc_disconnect(self, _: ServerConnection, __: Event):
        """
        The 'dccmsg' event contains the file data.
        :param _: The connection
        :param __: The 'dccmsg' event
        :return: None
        """
        if self.xdcc_file is not None:
            self.xdcc_file.close()
            print("Download complete")
        raise DownloadCompleted()
