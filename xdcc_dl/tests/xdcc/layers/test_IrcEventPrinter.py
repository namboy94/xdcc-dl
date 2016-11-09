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
import irc.events
from xdcc_dl.xdcc.layers.irc.IrcEventPrinter import IrcEventPrinter


class TestException(Exception):
    pass


class UnitTests(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_defined_methods(self):

        # noinspection PyUnusedLocal,PyShadowingNames
        def raise_exception(client, conn, event):

            client.on_privnotice(conn, event)
            client.on_privmsg(conn, event)
            client.on_ping(conn, event)
            client.on_ctcp(conn, event)

            raise TestException()

        IrcEventPrinter.on_welcome = raise_exception
        client = IrcEventPrinter("irc.namibsun.net", "random")

        try:
            client.start()
            self.assertTrue(False)
        except TestException:
            self.assertTrue(True)

    def test_auto_generated_methods(self):

        # noinspection PyUnusedLocal,PyShadowingNames
        def raise_exception(client, conn, event):

            for event in irc.events.all:
                self.assertTrue(callable(getattr(client, "on_" + event)))

            raise TestException()

        IrcEventPrinter.on_welcome = raise_exception
        client = IrcEventPrinter("irc.namibsun.net", "random")

        try:
            client.start()
            self.assertTrue(False)
        except TestException:
            self.assertTrue(True)

    def test_version_ctcp(self):

        # noinspection PyUnusedLocal,PyShadowingNames
        def raise_exception(client, conn, event):

            # noinspection PyUnusedLocal
            def print_check(string, formatting):
                self.assertEqual(string, "VERSION")

            client.logger.log = print_check
            event.arguments = ["VERSION"]
            client.on_ctcp(conn, event)
            raise TestException()

        IrcEventPrinter.on_welcome = raise_exception
        client = IrcEventPrinter("irc.namibsun.net", "random")

        try:
            client.start()
            self.assertTrue(False)
        except TestException:
            self.assertTrue(True)
