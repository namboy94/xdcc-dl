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
import requests
from typing import List
from bs4 import BeautifulSoup
from xdcc_dl.entities.XDCCPack import XDCCPack
from xdcc_dl.entities.IrcServer import IrcServer


def find_namibsun_packs(search_phrase: str) -> List[XDCCPack]:
    """
    Searches for XDCC Packs matching the specified search string on irc.namibsun.net:8000

    :param search_phrase: The search phrase to search for
    :return:              The list of found XDCC Packs
    """

    soup = BeautifulSoup(requests.get("http://irc.namibsun.net:8000").text, "html.parser")
    content = soup.select(".content")

    all_packs = []
    for i, item in enumerate(content):
        if item.text == search_phrase:
            all_packs.append(XDCCPack(IrcServer("irc.namibsun.net"), "xdcc_servbot", i + 1))
            all_packs[len(all_packs) - 1].set_filename(item.text)

    return all_packs
