"""LICENSE
Copyright 2016 Hermann Krumrey <hermann@krumreyh.com>
          2020 Jean Wicht <jean.wicht@gmail.com>

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
from xdcc_dl.entities.XDCCPack import XDCCPack
from xdcc_dl.entities.IrcServer import IrcServer


def find_ixirc_packs(search_phrase: str) -> List[XDCCPack]:
    """
    Searches for XDCC Packs matching the specified search string on ixirc.com
    Implementation courtesy of Jean Wicht <jean.wicht@gmail.com>.

    :param search_phrase: The search phrase to search for
    :return:              The list of found XDCC Packs
    """

    if not search_phrase:
        return []

    packs: List[XDCCPack] = []
    page_id = 0
    # the number of pages of results will be set properly in the request below
    page_count = 42
    while page_id < page_count:
        request = requests.get(
            "https://ixirc.com/api/",
            params={"q": search_phrase, "pn": str(page_id)},
        )

        if request.status_code != 200:
            return packs

        data = request.json()
        page_count = int(data["pc"])

        if "results" not in data:
            # no results
            return []

        for result in data["results"]:
            if "uname" not in result:
                # bot not online
                continue

            server = IrcServer(result["naddr"], result["nport"])
            pack = XDCCPack(server, result["uname"], int(result["n"]))
            pack.set_filename(result["name"])
            pack.set_size(result["sz"])
            packs.append(pack)

        page_id += 1  # next page

    return packs
