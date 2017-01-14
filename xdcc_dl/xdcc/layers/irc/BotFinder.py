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
# noinspection PyPep8Naming
from xdcc_dl.logging.LoggingTypes import LoggingTypes as LOG
from xdcc_dl.xdcc.layers.irc.IrcEventPrinter import IrcEventPrinter
from xdcc_dl.xdcc.layers.helpers.BotChannelMapper import BotChannelMapper


class BotNotFoundException(Exception):
    """
    An Exception to throw for when the WHOIS query does not return any results
    """
    pass


# noinspection PyUnusedLocal
class BotFinder(IrcEventPrinter):
    """
    Class that uses WHOIS queries to find and joins the channels a bot is a part of
    Layer 2 of the XDCC Bot
    """

    def on_welcome(self, connection: irc.client.ServerConnection, event: irc.client.Event) -> None:
        """
        The Welcome Event indicates that the server connection was established.
        A whois is sent to figure out which channels the bot resides in

        :param connection: the IRC Connection
        :param event:      the IRC Event
        :return:           None
        """
        # noinspection PyUnresolvedReferences
        super().on_welcome(connection, event)
        self.logger.log("Sending WHOIS command for " + self.current_pack.get_bot(), LOG.WHOIS_SEND)
        connection.whois(self.current_pack.get_bot())
        # -> Success: on_whoischannels or on_endofwhois
        # -> Failure: on_nosuchnick
        # Additional Effects:  ~> on_whoisuser
        #                      ~> on_whoisserver

    def on_whoischannels(self, connection: irc.client.ServerConnection, event: irc.client.Event) -> None:
        """
        A successful WHOIS query will result in this method being called. The bot will then attempt to join all
        channels the bot also joined

        :param connection: the IRC Connection
        :param event:      the IRC Event
        :return:           None
        """
        self.channel_join_required = True  # Some bots are not on any channel, and can be used
        # without joining any channel. If a whoischannels message is
        # received however, we need to join a channel

        self.logger.log("Received WHOIS information, bot resides in: " + event.arguments[1], LOG.WHOIS_SUCCESS)
        channels = event.arguments[1].split("#")
        channels.pop(0)

        new_channel_joined = False

        for channel in channels:
            channel = "#" + channel.split(" ")[0]

            if channel not in self.joined_channels:
                new_channel_joined = True
                self.joined_channels.append(channel)
                self.logger.log("Joining Channel " + channel, LOG.CHANNEL_JOIN_ATTEMPT)
                connection.join(channel)  # -> on_join

        if not new_channel_joined:
            self.logger.log("Channels joined already", LOG.CHANNEL_JOIN_SUCCESS)
            event.source = self.user.get_name()
            # noinspection PyUnresolvedReferences
            self.on_join(connection, event)

    def on_endofwhois(self, connection: irc.client.ServerConnection, event: irc.client.Event) -> None:
        """
        Checks the end of a WHOIS command if a channel join has occured or was even necessary
        If it was not necessary, starts the download

        :param connection: the IRC connection
        :param event:      the endofwhois event
        :return:           None
        """
        if not self.channel_join_required:

            if BotChannelMapper.has_mapping(self.current_pack.get_bot()):
                event.arguments = [None, BotChannelMapper.map(self.current_pack.get_bot())]
                self.on_whoischannels(connection, event)

            else:
                event.source = self.user.get_name()
                # noinspection PyUnresolvedReferences
                self.on_join(connection, event)  # Simulates a Channel Join if joining a channel is unnecessary
                # -> on_join

    def on_nosuchnick(self, connection: irc.client.ServerConnection, event: irc.client.Event) -> None:
        """
        This method is called if the WHOIS query fails, i.e. the bot does not exist on the IRC server
        It will forcefully abort the connection, which will then result in the bot skipping the current Pack

        :param connection: the IRC Connection
        :param event:      the IRC Event
        :return:           None
        """
        if event.arguments[0] == self.current_pack.get_bot():  # Make sure the failed WHOIS is for our bot
            self.logger.log("Bot " + self.current_pack.get_bot() + " does not exist on Server", LOG.WHOIS_NO_RESULT)
            raise BotNotFoundException()

    def on_whoisuser(self, connection: irc.client.ServerConnection, event: irc.client.Event) -> None:
        """
        Method called when a whoisuser command was received

        :param connection: the IRC Connection
        :param event:      the IRC Event
        :return:           None
        """
        message = ""
        for part in event.arguments:
            message += part + " "
        message = message.lstrip().rstrip()
        self.logger.log(message, LOG.WHOIS_USER)

    def on_whoisserver(self, connection: irc.client.ServerConnection, event: irc.client.Event) -> None:
        """
        Method called when a whoisserver command was received

        :param connection: the IRC Connection
        :param event:      the IRC Event
        :return:           None
        """
        message = ""
        for part in event.arguments:
            message += part + " "
        message = message.lstrip().rstrip()
        self.logger.log(message, LOG.WHOIS_SERVER)
