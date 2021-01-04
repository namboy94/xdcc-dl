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

# imports
import requests
from typing import List
from xdcc_dl.entities.XDCCPack import XDCCPack
from xdcc_dl.entities.IrcServer import IrcServer


def find_ixirc_packs(search_phrase: str) -> List[XDCCPack]:
    """
    Searches for XDCC Packs matching the specified search string on ixirc.com

    :param search_phrase: The search phrase to search for
    :return:              The list of found XDCC Packs
    """

    if not search_phrase:
        return []

    packs = []
    page_id = 0
    n_pages = 42 # the number of pages of results will be set properly in the request below
    while page_id < n_pages:
        r = requests.get("https://ixirc.com/api/", {"q": search_phrase, "pn": page_id})

        if r.status_code != 200:
            return packs

        j = r.json()
        n_pages = int(j["pc"])

        if "results" not in j:
            # no results
            return []

        for r in j["results"]:
            if "uname" not in r:
                # bot not online
                continue

            pack = XDCCPack(IrcServer(r["naddr"], r["nport"]), r["uname"], int(r["n"]))
            pack.set_filename(r["name"])
            pack.set_size(r["sz"])
            packs.append(pack)

        page_id += 1 # next page

    return packs
