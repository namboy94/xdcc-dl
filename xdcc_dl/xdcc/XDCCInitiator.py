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
import shlex
import irc.client
from typing import List
from xdcc_dl.entities.User import User
from xdcc_dl.logging.Logger import Logger
from xdcc_dl.entities.XDCCPack import XDCCPack
from xdcc_dl.entities.Progress import Progress
from xdcc_dl.xdcc.MessageSender import MessageSender
# noinspection PyPep8Naming
from xdcc_dl.logging.LoggingTypes import LoggingTypes as LOG


# noinspection PyUnusedLocal
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
        self.peer_address = None
        self.peer_port = None

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

        payload = shlex.split(event.arguments[1])

        if payload[0] == "SEND":
            self.dcc_send_handler(payload, connection)
        elif payload[1] == "ACCEPT":
            self.dcc_accept_handler(payload, connection)

    def dcc_send_handler(self, ctcp_arguments: List[str], connection: irc.client.ServerConnection) -> None:
        """
        Handles incoming CTCP DCC SENDs. Initiates a download or RESUME request.

        :param ctcp_arguments: The CTCP Arguments
        :param connection:     The connection to use for DCC connections
        :return:               None
        """
        self.logger.log("Handling DCC SEND Handshake", LOG.DCC_SEND_HANDSHAKE)

        filename = ctcp_arguments[1]
        self.peer_address = irc.client.ip_numstr_to_quad(ctcp_arguments[2])
        self.peer_port = int(ctcp_arguments[3])
        size = int(ctcp_arguments[4])

        self.progress.set_single_progress_total(int(size))
        self.current_pack.set_filename(filename)

        if os.path.exists(self.current_pack.get_filepath()):

            self.logger.log("Requesting DCC RESUME", LOG.DCC_RESUME_REQUEST)

            position = os.path.getsize(self.current_pack.get_filepath())
            self.progress.set_single_progress(position)

            resume_parameter = "\"" + filename + "\" " + str(self.peer_port) + " " + str(position)
            connection.ctcp("DCC RESUME", self.current_pack.get_bot(), resume_parameter)

        else:

            self.logger.log("Starting Download of " + filename, LOG.DOWNLOAD_START)

            self.file = open(self.current_pack.get_filepath(), "wb")
            self.dcc_connection = self.dcc_connect(self.peer_address, self.peer_port, "raw")
            self.download_started = True

    def dcc_accept_handler(self, ctcp_arguments: List[str], connection: irc.client.ServerConnection) -> None:
        """
        Handles DCC ACCEPT messages. Resumes a download.

        :param ctcp_arguments: The CTCP arguments
        :param connection:     The connection to use for DCC connections
        :return:               None
        """
        self.logger.log("DCC RESUME succeeded", LOG.DCC_RESUME_SUCCESS)
        self.logger.log("Resuming Download of " + self.current_pack.get_filepath(), LOG.DOWNLOAD_RESUME)

        self.file = open(self.current_pack.get_filepath(), "ab")
        self.dcc_connection = self.dcc_connect(self.peer_address, self.peer_port, "raw")
        self.download_started = True
