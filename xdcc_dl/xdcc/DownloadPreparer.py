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
import irc.client
from typing import List
from xdcc_dl.entities.User import User
from xdcc_dl.logging.Logger import Logger
from xdcc_dl.entities.XDCCPack import XDCCPack
from xdcc_dl.entities.Progress import Progress
from xdcc_dl.entities.IrcServer import IrcServer
from xdcc_dl.xdcc.IrcEventPrinter import IrcEventPrinter


class DownloadPreparer(IrcEventPrinter):
    """
    Class that prepares an (or multiple) XDCC Downloads
    Layer 2 of the XDCC Bot
    """

    def __init__(self, packs: List[XDCCPack], user: User, logger: Logger, progress: Progress) -> None:
        """
        Initializes a Download Preparer.

        :param packs:    the packs to download
        :param user:     the username to use
        :param logger:   the logger to use
        :param progress: the Progress object to keep track of the download progress
        """
        super().__init__(packs[0].get_server(), user, logger)
        self.packs = packs
        self.progress = progress
        self.current_pack = packs[0]  # Could also be = None, but decided on packs[0] for IDE purposes

    def start(self) -> None:
        """
        Starts the download progress

        :return: None
        """
        for pack in self.packs:
            self.server = pack.get_server()
            self.current_pack = pack
            super().start()  # -> on_welcome

    def on_welcome(self, connection: irc.client.ServerConnection, event: irc.client.Event) -> None:
        """
        The Welcome Event indicates that the server connection was established.
        A whois is sent to figure out which channels the bot resides in

        :param connection: the IRC Connection
        :param event:      the IRC Event
        :return: None
        """
        # noinspection PyUnresolvedReferences
        super().on_welcome(connection, event)
        self.logger.log("Sending WHOIS command for " + self.current_pack.get_bot(), LOG.WHOIS_SEND)
        connection.whois(self.current_pack.get_bot())

    def on_whoischannels(self, connection: irc.client.ServerConnection, event: irc.client.Event) -> None:
        """
        A successful WHOIS query will result in this method being called. The bot will then attempt to join all
        channels the bot also joined

        :param connection: the IRC Connection
        :param event:      the IRC Event
        :return: None
        """
        self.logger.log("Received WHOIS information, bot resides in: " + event.arguments[1], LOG.WHOIS_SUCCESS)
        channels = event.arguments[1].split("#")
        channels.pop(0)

        for channel in channels:
            self.join()