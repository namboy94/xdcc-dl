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
import irc.events
# noinspection PyUnresolvedReferences,PyPep8Naming
from xdcc_dl.logging.LoggingTypes import LoggingTypes as LOG
from xdcc_dl.xdcc.layers.irc.BaseIrcClient import BaseIrclient


def create_event_printer(event: str, formatting: str, show_tag: bool = False) -> str:
    """
    Creates a new method definition for an on_event method that can then be integrated using exec

    :param event:      The name of the event on which this method is called
    :param formatting: The formatting from LOG, but as a string
    :param show_tag:   Determines if an 'on_event" string should be printed beforehand
    :return:           The method as an executable string
    """
    method_definition = "def on_" + event + "(self, connection, event):\n"
    if show_tag:
        method_definition += "    self.logger.log(\"on_" + event + "\", LOG.EVENT)\n"
    method_definition += "    print_args = \"\"\n"
    method_definition += "    for arg in event.arguments:\n"
    method_definition += "        print_args += arg + \" \"\n"
    method_definition += "    print_args = print_args.rstrip().lstrip()\n"
    method_definition += "    self.logger.log(print_args, " + formatting + ")"
    return method_definition


# noinspection PyMethodMayBeStatic,PyUnusedLocal
class IrcEventPrinter(BaseIrclient):
    """
    Class that prints output to the console for every type of IRC event defined by the irc library
    Layer 1 of the XDCC Bot
    """

    # This assigns a method to all event types that are supported by the IRC library.
    # They print the type of event and its parameters
    for event in irc.events.all:
        if event != "disconnect":
            method = create_event_printer(event, "LOG.EVENT_TEXT", True)
            exec(method)

    # Here are some more specialized ones

    # Prints the server greeting
    for event in ["welcome", "yourhost", "created", "myinfo", "featurelist", "luserclient", "luserop",
                  "luserunknown", "luserchannels", "luserme", "n_local", "n_global", "modstart"]:
        exec(create_event_printer(event, "LOG.WELCOME", False))

    # Message of the Day
    for event in ["motd", "motdstart", "endofmotd"]:
        exec(create_event_printer(event, "LOG.MESSAGE_OF_THE_DAY", False))

    # Here we manually define the more interesting methods:

    def on_privnotice(self, connection: irc.client.ServerConnection, event: irc.client.Event) -> None:
        """
        Prints Private Notices

        :param connection: the IRC Connection
        :param event:      the IRC Event
        :return:           None
        """
        self.logger.log(event.arguments[0], LOG.PRIVATE_NOTICE)

    def on_privmsg(self, connection: irc.client.ServerConnection, event: irc.client.Event) -> None:
        """
        Prints Private Messages

        :param connection: the IRC Connection
        :param event:      the IRC Event
        :return:           None
        """
        self.logger.log(event.source + ": " + event.arguments[0], LOG.PRIVATE_MESSAGE)

    def on_pubnotice(self, connection: irc.client.ServerConnection, event: irc.client.Event) -> None:
        """
        Prints Public Notices

        :param connection: the IRC Connection
        :param event:      the IRC Event
        :return:           None
        """
        self.logger.log(event.source + ": " + event.arguments[0], LOG.PUBLIC_NOTICE)

    def on_pubmsg(self, connection: irc.client.ServerConnection, event: irc.client.Event) -> None:
        """
        Prints Public Messages

        :param connection: the IRC Connection
        :param event:      the IRC Event
        :return:           None
        """
        self.logger.log(event.source + ": " + event.arguments[0], LOG.PUBLIC_MESSAGE)

    def on_ping(self, connection: irc.client.ServerConnection, event: irc.client.Event) -> None:
        """
        Prints Pings

        :param connection: the IRC Connection
        :param event:      the IRC Event
        :return:           None
        """
        self.logger.log("PING: " + event.arguments[0], LOG.PING)

    def on_ctcp(self, connection: irc.client.ServerConnection, event: irc.client.Event) -> None:
        """
        Prints Client-To-Client_Protocol 'Version' Messages

        :param connection: the IRC Connection
        :param event:      the IRC Event
        :return:           None
        """
        if event.arguments[0] == "VERSION":
            self.logger.log(event.arguments[0], LOG.CTCP_VERSION)
            return
