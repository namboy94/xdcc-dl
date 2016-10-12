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
from jaraco.stream import buffer
from xdcc_dl.entities.User import User
from xdcc_dl.logging.Logger import Logger
from xdcc_dl.entities.IrcServer import IrcServer
from xdcc_dl.xdcc.ConnectionStates import ConnectionStates
# noinspection PyPep8Naming
from xdcc_dl.logging.LoggingTypes import LoggingTypes as LOG


class IgnoreErrorsBuffer(buffer.DecodingLineBuffer):
    """
    Decoding Buffer for the IRC Client that ignores any errors, like UTF8
    decoding errors, which may appear with some messages.
    """
    def handle_exception(self) -> None:
        """
        Handles the Exception itself, does nothing.
        :return: None
        """
        pass


class Disconnect(Exception):
    """
    Class that gets raised when a normal disconnect occurs
    """
    pass


class BaseIrclient(irc.client.SimpleIRCClient, ConnectionStates):
    """
    The Base IRC Client that defines the necessary features that an IRC Client must be able to do.
    Layer 0 of the XDCC Bot
    """

    def __init__(self, irc_server: IrcServer, user: User, logger: Logger):
        """
        Initializes the Client's Server Connection Information and disables Buffer Errors

        :param irc_server: The IRC Server to which th client will attempt to connect to
        :param user:       The User to log in to the IRC Server with
        :param logger:     The logger used to print informational messages to the console
        """
        super().__init__()
        ConnectionStates.__init__(self)

        self.logger = logger

        irc.client.ServerConnection.buffer_class = IgnoreErrorsBuffer
        irc.client.SimpleIRCClient.buffer_class = IgnoreErrorsBuffer

        self.server = irc_server
        self.user = user

        self.server_address = irc_server.get_address()
        self.server_port = irc_server.get_port()
        self.user_name = user.get_name()

    def connect(self) -> None:
        """
        Connects the IRC Client to the IRC Server

        :return: None
        """
        self.logger.log("Connecting to server:  " + self.server_address,   LOG.CONNECTION_ATTEMPT)
        self.logger.log("Using Port:            " + str(self.server_port), LOG.CONNECTION_ATTEMPT)
        self.logger.log("As User:               " + self.user_name,        LOG.CONNECTION_ATTEMPT)

        try:
            super().connect(self.server_address, int(self.server_port), self.user_name)
            self.logger.log("Established Connection to Server", LOG.CONNECTION_SUCCESS)
            self.connected_to_server = True
        except irc.client.ServerConnectionError:
            self.logger.log("Failed to connect to Server", LOG.CONNECTION_FAILURE)

    def start(self) -> None:
        """
        Starts the IRC Connection

        :return: None
        """
        try:
            self.connect()
            super().start()
        except Disconnect:
            pass

    def on_disconnect(self, connection: irc.client.ServerConnection, event: irc.client.Event) -> None:
        """
        Method called whenever the IRC connection is disconnected

        :param connection: the IRC Connection
        :param event:      the IRC Event
        :return:           None
        """
        raise Disconnect()


if __name__ == '__main__':

    import sys
    sys.argv.pop(0)
    address, username, verbosity = sys.argv

    BaseIrclient(IrcServer(address), User(username), Logger(int(verbosity))).start()
