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
import irc.events
from xdcc_dl.xdcc.layers.irc.IrcEventPrinter import IrcEventPrinter


class TestException(Exception):
    pass


class UnitTests(unittest.TestCase):

    def setUp(self):
        self.client = IrcEventPrinter

    def tearDown(self):
        self.client.quit()

    def test_defined_methods(self):

        class Tester(IrcEventPrinter):
            def on_welcome(self, conn, event):

                self.on_privnotice(conn, event)
                self.on_privmsg(conn, event)
                self.on_pubnotice(conn, event)
                self.on_pubmsg(conn, event)
                self.on_ping(conn, event)
                self.on_ctcp(conn, event)
                raise TestException()

        self.client = Tester("irc.namibsun.net", "random")
        try:
            self.client.start()
            self.assertTrue(False)
        except TestException:
            self.assertTrue(True)

    def test_auto_generated_methods(self):

        class Tester(IrcEventPrinter):

            assertions_true = True

            # noinspection PyUnusedLocal
            def on_welcome(self, conn, event):

                for event in irc.events.all:
                    self.assertions_true = self.assertions_true and callable(getattr(self, "on_" + event))
                raise TestException()

        self.client = Tester("irc.namibsun.net", "random")

        try:
            self.client.start()
            self.assertTrue(False)
        except TestException:
            self.assertTrue(self.client.assertions_true)

    def test_version_ctcp(self):

        class Tester(IrcEventPrinter):

            assertions_true = False

            def on_welcome(self, conn, event):

                event.arguments = ["VERSION"]
                self.on_ctcp(conn, event)

                raise TestException()

            def on_ctcp(self, conn, event):
                super().on_ctcp(conn, event)
                self.assertions_true = event.arguments[0] == "VERSION"

        self.client = Tester("irc.namibsun.net", "random")

        try:
            self.client.start()
            self.assertTrue(False)
        except TestException:
            self.assertTrue(self.client.assertions_true)
