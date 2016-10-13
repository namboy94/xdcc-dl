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
import os
import irc.client
from typing import List
from xdcc_dl.entities.Progress import Progress
from xdcc_dl.entities.User import User
from xdcc_dl.entities.XDCCPack import XDCCPack
from xdcc_dl.logging.Logger import Logger
from xdcc_dl.xdcc.MessageSender import MessageSender


class XDCCInitiator(MessageSender):
    """
    Initiates the XDCC Connection.
    Layer 4 of the XDCC Bot
    """

    def __init__(self, packs: List[XDCCPack], user: User, logger: Logger, progress: Progress) -> None:
        """
        Initializes the XDCC Initiator object. Defines local DCC connection and the opened download file

        :param packs:    the packs to download
        :param user:     the username to use
        :param logger:   the logger to use
        :param progress: the Progress object to keep track of the download progress
        """
        super().__init__(packs, user, logger, progress)
        self.file = None
        self.dcc_connection = None

    def on_ctcp(self, connection: irc.client.ServerConnection, event: irc.client.Event):
        """
        Client-to-Client Connection which initiates the XDCC handshake

        :param connection: the IRC Connection
        :param event:      the IRC Event
        :return:           None
        """
        super().on_ctcp(connection, event)

        if event.arguments[0] != "DCC":
            return

        self.logger.log("Initiated XDCC Handshake")

        payload = event.arguments[1].split(" ")

        if len(payload) == 5:
            command, filename, peer_address, peer_port, size = payload
        elif len(payload) == 6:
            # TOD check if this actually works that way
            command, filename, peer_address, peer_port, size, dummy = payload
        else:
            self.logger.log("Invalid amount of arguments")
            return

        peer_address = irc.client.ip_numstr_to_quad(peer_address)
        peer_port = int(peer_port)

        self.progress.set_single_progress_total(int(size))
        self.current_pack.set_filename(filename)

        # Check if the file already exists. If it does, delete it beforehand
        if os.path.exists(self.current_pack.get_filepath()):
            # TODO Continue
            pass

        else:
            self.file = open(self.current_pack.get_filepath(), "wb")
            self.dcc_connection = self.dcc_connect(peer_address, peer_port, "raw")
            self.logger.log("Established DCC connection")
            self.download_started = True


if __name__ == "__main__":

    from xdcc_dl.entities.IrcServer import IrcServer
    xpacks = [XDCCPack(IrcServer("irc.rizon.net"), "ginpachi-sensei", 1, "/home/hermann/testing/test.txt")]
    XDCCInitiator(xpacks, User("Heramann"), Logger(5), Progress(len(xpacks))).start()
