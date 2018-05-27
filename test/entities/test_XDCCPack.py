"""LICENSE
Copyright 2016 Hermann Krumrey <hermann@krumreyh.com>

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
LICENSE"""

from unittest import TestCase
from xdcc_dl.entities.XDCCPack import XDCCPack
from xdcc_dl.entities.IrcServer import IrcServer


class XDCCPackTest(TestCase):
    """
    Test case that tests the functionality of the XDCCPack class
    """

    def test_from_message(self):
        single = XDCCPack.from_xdcc_message("/msg Bot1 xdcc send #1")
        _range = XDCCPack.from_xdcc_message("/msg Bot2 xdcc send #2-5")
        range_step = XDCCPack.from_xdcc_message("/msg Bot3 xdcc send #6-10;2")
        commas = XDCCPack.from_xdcc_message("/msg Bot4 xdcc send #11,111,1111")

        rizon = IrcServer("irc.rizon.net")

        self.assertEqual(single[0], XDCCPack(rizon, "Bot1", 1))

        for x in range(2, 6):
            self.assertEqual(_range[x - 2], XDCCPack(rizon, "Bot2", x))

        i = 0
        for x in range(6, 11, 2):
            self.assertEqual(range_step[i], XDCCPack(rizon, "Bot3", x))
            i += 1

        commas_value = "11"
        for pack in commas:
            self.assertEqual(pack, XDCCPack(rizon, "Bot4", int(commas_value)))
            commas_value += "1"
