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
import unittest
from xdcc_dl.metadata import SentryLogger
from xdcc_dl.entities.XDCCPack import XDCCPack
from xdcc_dl.entities.IrcServer import IrcServer
from xdcc_dl.xdcc.layers.helpers.BotChannelMapper import BotChannelMapper
from xdcc_dl.xdcc.layers.xdcc.XDCCInitiator import XDCCInitiator, NoValidWhoisQueryException


class TestException(Exception):
    pass


class UnitTests(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_dcc_check(self):

        class Tester(XDCCInitiator):

            def on_welcome(self, conn, event):
                event.arguments = ["NOTDCC"]
                self.on_ctcp(conn, event)
                raise TestException()

        try:
            Tester("irc.namibsun.net", "random").start()
            self.assertTrue(False)
        except TestException:
            self.assertTrue(True)

    def test_missing_whois(self):
        class DummySentry(object):
            # noinspection PyPep8Naming
            def captureMessage(self, string):
                pass

        BotChannelMapper.bot_channel_map = {}
        SentryLogger.sentry = DummySentry()

        try:
            initiator = XDCCInitiator("irc.rizon.net", "random")
            initiator.current_pack = XDCCPack(IrcServer("irc.rizon.net"), "HelloKitty", 1)
            initiator.start()
            self.assertTrue(False)
        except NoValidWhoisQueryException:
            self.assertTrue(True)
