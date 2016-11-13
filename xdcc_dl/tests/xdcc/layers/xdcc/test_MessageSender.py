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
from xdcc_dl.xdcc.layers.xdcc.MessageSender import MessageSender


class TestException(Exception):
    pass


class UnitTests(unittest.TestCase):

    def setUp(self):
        self.client = MessageSender

    def tearDown(self):
        self.client.quit()

    def test_logging(self):

        class Tester(MessageSender):
            def on_welcome(self, conn, event):

                self.on_currenttopic(conn, event)
                self.on_topicinfo(conn, event)
                self.on_quit(conn, event)
                self.on_part(conn, event)
                self.on_kick(conn, event)
                self.on_mode(conn, event)
                self.on_action(conn, event)
                self.on_nick(conn, event)

                raise TestException()

        self.client = Tester("irc.namibsun.net", "random")
        try:
            self.client.start()
            self.assertFalse(True)
        except TestException:
            self.assertTrue(True)

    def test_other_user_joined_channel(self):

        class Tester(MessageSender):
            def on_welcome(self, conn, event):

                event.source = "Other User"
                self.on_join(conn, event)

            def on_join(self, conn, event):
                super().on_join(conn, event)
                raise TestException()

        self.client = Tester("irc.namibsun.net", "random")
        try:
            self.client.start()
            self.assertFalse(True)
        except TestException:
            self.assertTrue(True)

    def test_joining_second_channel(self):

        class Tester(MessageSender):
            def on_welcome(self, conn, event):

                self.channel_joined = True
                event.source = self.user.get_name()
                self.on_join(conn, event)
                raise TestException()

        self.client = Tester("irc.namibsun.net", "random")
        try:
            self.client.start()
            self.assertFalse(True)
        except TestException:
            self.assertTrue(True)
