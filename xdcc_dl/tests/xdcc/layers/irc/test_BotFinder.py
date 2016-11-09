"""
LICENSE:
Copyright 2015,2016 Hermann Krumrey

This file is part of toktokkie.

    toktokkie is a program that allows convenient managing of various
    local media collections, mostly focused on video.

    toktokkie is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    toktokkie is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with toktokkie.  If not, see <http://www.gnu.org/licenses/>.
LICENSE
"""

# imports
import unittest
from xdcc_dl.entities.XDCCPack import XDCCPack
from xdcc_dl.entities.IrcServer import IrcServer
from xdcc_dl.xdcc.layers.irc.BotFinder import BotFinder
from xdcc_dl.xdcc.layers.irc.BaseIrcClient import Disconnect


class TestException(Exception):
    pass


class UnitTests(unittest.TestCase):

    def setUp(self):
        self.client = BotFinder

    def tearDown(self):
        self.client.quit()

    def test_whois_query(self):

        class Tester(BotFinder):

            joined_correct_channel = False
            all_whois_counter = 0

            def on_welcome(self, conn, event):
                self.connection.whois("xdcc_servbot")

            # noinspection PyUnusedLocal
            def on_join(self, conn, event):
                if event.source.startswith(self.user.get_name()):
                    self.joined_correct_channel = event.target.lower() == "#bots"

                    if self.all_whois_counter == 3:
                        raise TestException()

            def on_whoischannels(self, conn, event):
                self.all_whois_counter += 1
                super().on_whoischannels(conn, event)

            def on_whoisserver(self, conn, event):
                self.all_whois_counter += 1
                super().on_whoisserver(conn, event)

            def on_endofwhois(self, conn, event):
                self.all_whois_counter += 1
                super().on_endofwhois(conn, event)

                if self.joined_correct_channel:
                    raise TestException()

        self.client = Tester("irc.namibsun.net", "random")

        try:
            self.client.start()
            self.assertTrue(False)
        except TestException:
            self.assertTrue(self.client.joined_correct_channel)
            self.assertEqual(self.client.all_whois_counter, 3)

    def test_invalid_whois_query(self):

        class Tester(BotFinder):

            incorrect_nick_detected = False

            def on_welcome(self, conn, event):
                self.current_pack = XDCCPack(IrcServer("irc.namibsun.net"), "notexistingbot", 1)
                self.connection.whois("notexistingbot")

            # noinspection PyUnusedLocal
            def on_nosuchnick(self, conn, event):
                try:
                    super().on_nosuchnick(conn, event)
                except Disconnect:
                    self.incorrect_nick_detected = True
                raise TestException()

        self.client = Tester("irc.namibsun.net", "random")

        try:
            self.client.start()
            self.assertTrue(False)
        except TestException:
            self.assertTrue(self.client.incorrect_nick_detected)

    def test_stray_whois(self):

        class Tester(BotFinder):

            stray_whois_detected = False

            def on_welcome(self, conn, event):
                self.current_pack = XDCCPack(IrcServer("irc.namibsun.net"), "xdcc_servbot", 1)
                self.connection.whois("notexistingbot")

            # noinspection PyUnusedLocal
            def on_nosuchnick(self, conn, event):
                super().on_nosuchnick(conn, event)
                self.stray_whois_detected = True
                raise TestException()

        self.client = Tester("irc.namibsun.net", "random")

        try:
            self.client.start()
            self.assertTrue(False)
        except TestException:
            self.assertTrue(self.client.stray_whois_detected)

    def test_channel_less_whois_query(self):

        class Tester(BotFinder):

            dummy_channel_joined = False

            def on_welcome(self, conn, event):
                self.connection.whois("channelless_bot")

            # noinspection PyUnusedLocal
            def on_nosuchnick(self, conn, event):
                self.on_endofwhois(conn, event)

            # noinspection PyUnusedLocal
            def on_join(self, conn, event):
                if event.source == self.user.get_name():
                    self.dummy_channel_joined = True
                    raise TestException()

        self.client = Tester("irc.namibsun.net", "random")

        try:
            self.client.start()
            self.assertTrue(False)
        except TestException:
            self.assertTrue(self.client.dummy_channel_joined)
