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

import requests
from typing import List
from bs4 import BeautifulSoup
from xdcc_dl.entities.XDCCPack import XDCCPack
from xdcc_dl.entities.IrcServer import IrcServer
from puffotter.units import byte_string_to_byte_count


def find_nibl_packs(search_phrase: str) -> List[XDCCPack]:
    """
    Searches for XDCC Packs matching the specified search string on nibl.co.uk

    :param search_phrase: The search phrase to search for
    :return:              The list of found XDCC Packs
    """
    query = "+".join(search_phrase.split(" "))
    url = f"https://nibl.co.uk/search?query={query}"
    html = requests.get(url).text

    content = BeautifulSoup(html, "html.parser")
    rows = content.find_all("tr")

    if len(rows) == 0:
        return []

    header = rows.pop(0)
    keys = [x.text for x in header.find_all("th")]
    results = [
        {
            keys[i]: column.text.strip()
            for i, column in enumerate(row.find_all("td"))
        }
        for row in rows
    ]

    server = IrcServer("irc.rizon.net")
    packs = []
    for result in results:
        pack = XDCCPack(server, result["Bot"], int(result["Pack"]))
        pack.set_size(byte_string_to_byte_count(result["Size"]))
        pack.set_filename(result["Filename"])
        packs.append(pack)
    return packs
