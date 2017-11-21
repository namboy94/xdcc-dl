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

# imports
import unittest
from xdcc_dl.entities.IrcServer import IrcServer


class UnitTests(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_server_entity_constructor(self):

        server = IrcServer("irc.namibsun.net")
        self.assertEqual(server.get_address(), "irc.namibsun.net")
        self.assertEqual(server.get_port(), 6667)

    def test_server_entity_constructor_with_port(self):

        server = IrcServer("irc.namibsun.net", 9000)
        self.assertEqual(server.get_address(), "irc.namibsun.net")
        self.assertEqual(server.get_port(), 9000)
