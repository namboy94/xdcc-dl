"""
Copyright 2016-2017 Hermann Krumrey

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


class BotChannelMapper(object):
    """
    Class that maps bots with non-standard whois responses to a channel
    """

    bot_channel_map = {"HelloKitty": "#horriblesubs"}

    @staticmethod
    def has_mapping(botname: str) -> bool:
        """
        Checks if a bot is mapped to a channel in this class

        :param botname: The bot's name
        :return:        True, if it has a mapping, false otherwise
        """
        return botname in BotChannelMapper.bot_channel_map.keys()

    @staticmethod
    def map(botname: str) -> str:
        """
        Maps a bot to a channel name

        :param botname: The bot's name
        :return:        The mapped channel name
        """
        return BotChannelMapper.bot_channel_map[botname]
