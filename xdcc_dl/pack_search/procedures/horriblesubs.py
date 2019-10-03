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
import cfscrape
from typing import List, Dict
from xdcc_dl.entities.XDCCPack import XDCCPack
from xdcc_dl.entities.IrcServer import IrcServer


def find_horriblesubs_packs(search_phrase: str) -> List[XDCCPack]:
    """
    Method that conducts the xdcc pack search for xdcc.horriblesubs.info

    :return: the search results as a list of XDCCPack objects
    """
    if not search_phrase:
        return []

    search_query = search_phrase.replace(" ", "%20")
    search_query = search_query.replace("!", "%21")

    url = "http://xdcc.horriblesubs.info/search.php?t=" + search_query
    scraper = cfscrape.create_scraper()
    results = scraper.get(url).text.split(";")

    packs = []
    for result in results:

        try:
            result = parse_result(result)
            botname = result["b"]
            filename = result["f"]
            filesize = int(result["s"])
            packnumber = int(result["n"])
            pack = XDCCPack(IrcServer("irc.rizon.net"), botname, packnumber)
            pack.set_filename(filename)
            pack.set_size(filesize)
            packs.append(pack)

        except IndexError:  # In case the line is not parseable
            pass

    return packs


def parse_result(result: str) -> Dict[str, str]:
    """
    Turns the weird horriblesubs response syntax into a useable dictionary
    :param result: The result to parse
    :return: The result as a dictionary
    """

    # Result should look like this:
    # {b: "Bot", n:filesize, s:packnumber, f:"filename"}

    data = {}
    result = result.split("=", 1)[1].strip()
    result = result[1:-1]  # Trim away curly braces

    current_key = None
    for position, segment in enumerate(result.split("\"")):

        if segment == "":
            continue

        if position % 2 == 0:
            # Segment is not a string, must be evaluated further
            for part in segment.split(","):

                if part == "":
                    continue

                key, content = part.split(":", 1)
                current_key = key.strip()
                if content != "":
                    data[current_key.strip()] = content.strip()

        else:
            # Segment is a string
            data[str(current_key)] = segment

    return data
