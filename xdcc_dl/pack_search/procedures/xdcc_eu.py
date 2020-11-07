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


def find_xdcc_eu_packs(search_phrase: str) -> List[XDCCPack]:
    """
    Method that conducts the xdcc pack search for xdcc.eu

    :return: the search results as a list of XDCCPack objects
    """
    url = "https://www.xdcc.eu/search.php?searchkey=" + search_phrase
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    entries = soup.select("tr")
    entries.pop(0)

    packs = []
    for entry in entries:
        parts = entry.select("td")
        info = parts[1].select("a")[1]
        server = IrcServer(info["data-s"])
        pack_message = info["data-p"]
        bot, pack_number = pack_message.split(" xdcc send #")

        size = byte_string_to_byte_count(parts[5].text)
        filename = parts[6].text

        pack = XDCCPack(server, bot, int(pack_number))
        pack.set_size(size)
        pack.set_filename(filename)

        packs.append(pack)

    return packs
