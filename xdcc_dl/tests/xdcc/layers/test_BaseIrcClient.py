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
from nose.tools import timed
from xdcc_dl.xdcc.layers.irc.BaseIrcClient import BaseIrclient, NetworkError


class TestException(Exception):
    pass


class UnitTests(unittest.TestCase):

    def setUp(self):
        self.client = BaseIrclient

    def tearDown(self):
        self.client.quit()

    def test_faulty_server(self):

        self.client = BaseIrclient("gitlab.namibsun.net", "random")
        try:
            self.client.start()
            self.assertTrue(False)
        except NetworkError as e:
            self.assertEqual(str(e), "Failed to connect to Server")

    @timed(3)
    def test_server_connect(self):

        class Tester(BaseIrclient):

            # noinspection PyMethodMayBeStatic
            def on_welcome(self, conn, event):
                raise TestException()

        self.client = Tester("irc.namibsun.net", "random")

        try:
            self.client.start()
            self.assertTrue(False)
        except TestException:
            self.assertTrue(True)

    @timed(3)
    def test_on_banned(self):

        class Tester(BaseIrclient):
            def on_welcome(self, conn, event):
                self.on_error(conn, event)

        self.client = Tester("irc.namibsun.net", "random")

        try:
            self.client.start()
            self.assertTrue(False)
        except NetworkError as e:
            self.assertEqual(str(e), "Failed to connect due to a ban")
