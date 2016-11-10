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
import irc.client
import jaraco.logging
from jaraco.stream import buffer
from xdcc_dl.entities.User import User
from xdcc_dl.logging.Logger import Logger
from xdcc_dl.entities.IrcServer import IrcServer
from xdcc_dl.xdcc.layers.helpers.Variables import Variables
# noinspection PyPep8Naming
from xdcc_dl.logging.LoggingTypes import LoggingTypes as LOG
from xdcc_dl.xdcc.layers.helpers.ConnectionStates import ConnectionStates


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
        pass  # pragma: no cover


class Disconnect(Exception):
    """
    Class that gets raised when a normal disconnect occurs
    """
    pass


class NetworkError(Exception):
    """
    Class that gets raised when a network error occurs
    """
    pass


class Banned(Exception):
    """
    Exception that gets raised when a network error occurs
    """
    pass


class BaseIrclient(irc.client.SimpleIRCClient, ConnectionStates, Variables):
    """
    The Base IRC Client that defines the necessary features that an IRC Client must be able to do.
    Layer 0 of the XDCC Bot
    """

    def __init__(self, server: IrcServer or str, user: User or str, logger: Logger or int = 0):
        """
        Initializes the Client's Server Connection Information and disables Buffer Errors
        The parameters can all be initialized with either a string/int representing the object's
        main value or the classes themselves

        :param server: The IRC Server to which th client will attempt to connect to
                       If a string was provided, create IrcServer with default ort 6667
        :param user:   The User to log in to the IRC Server with
                       If a string was provided, create user object with that username
        :param logger: The logger used to print informational messages to the console
                       If an int was provided, creates a standard console logger with the specified verbosity level
        """
        super().__init__()
        Variables.__init__(self)
        ConnectionStates.__init__(self)

        jaraco.logging.log_level("0")

        irc.client.ServerConnection.buffer_class = IgnoreErrorsBuffer
        irc.client.SimpleIRCClient.buffer_class = IgnoreErrorsBuffer

        self.user = user if user.__class__ == User else User(user)
        self.server = server if server.__class__ == IrcServer else IrcServer(server)
        self.logger = logger if logger.__class__ == Logger else Logger(logger)

    def connect(self) -> None:
        """
        Connects the IRC Client to the IRC Server

        :raises: NetworkError if the connection to the server did not succeed
        :return: None
        """
        self.logger.log("Connecting to server:  " + self.server.get_address(), LOG.CONNECTION_ATTEMPT)
        self.logger.log("Using Port:            " + str(self.server.get_port()), LOG.CONNECTION_ATTEMPT)
        self.logger.log("As User:               " + self.user.get_name(), LOG.CONNECTION_ATTEMPT)

        super().connect(self.server.get_address(), int(self.server.get_port()), self.user.get_name())
        self.logger.log("Established Connection to Server", LOG.CONNECTION_SUCCESS)
        self.connected_to_server = True

    def start(self) -> None:
        """
        Starts the IRC Connection

        :raises: NetworkError if the connection to the server did not succeed
        :return: None
        """
        network_error = ""

        try:
            self.connect()
            super().start()
        except irc.client.ServerConnectionError:
            self.logger.log("Failed to connect to Server", LOG.CONNECTION_FAILURE)
            network_error = "Failed to connect to Server"
        except Banned:
            self.logger.log("Failed to connect due to a ban", LOG.BANNED)
            network_error = "Failed to connect due to a ban"
        except Exception as e:
            try:
                self.quit()
            except (Disconnect, irc.client.ServerNotConnectedError):
                pass
            if str(type(e)) != "<class 'xdcc_dl.xdcc.layers.irc.BaseIrcClient.Disconnect'>":
                self.connected_to_server = False
                raise e

        try:
            self.quit()
        except Disconnect:
            pass

        if network_error:
            raise NetworkError(network_error)

    def quit(self) -> None:
        """
        Forcibly closes the connection

        :return: None
        """

        try:
            self.connection.disconnect()
            self.connection.quit()
        except (Disconnect, irc.client.ServerNotConnectedError):
            try:
                self.connection.quit()
            except (Disconnect, irc.client.ServerNotConnectedError):
                pass

        if self.connected_to_server:
            self.connected_to_server = False
            raise Disconnect()

    # noinspection PyMethodMayBeStatic
    def on_disconnect(self, connection: irc.client.ServerConnection, event: irc.client.Event) -> None:
        """
        Method called whenever the IRC connection is disconnected

        :param connection: the IRC Connection
        :param event:      the IRC Event
        :raises:           Disconnect, when the connection was disconnected by non-fatal means
        :return:           None
        """
        raise Disconnect()

    # noinspection PyMethodMayBeStatic
    def on_error(self, connection: irc.client.ServerConnection, event: irc.client.Event) -> None:
        """
        Method called whenever the IRC connection throws an error event, which means that the user is banned

        :param connection: the IRC Connection
        :param event:      the IRC Event
        :raises:           Disconnect, when the connection was disconnected by non-fatal means
        :return:           None
        """
        raise Banned()
