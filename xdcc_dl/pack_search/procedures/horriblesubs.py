"""LICENSE
Copyright 2016 Hermann Krumrey

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
from typing import List
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
            botname = get_attribute(result, "b")
            filename = get_attribute(result, "f")
            filesize = get_attribute(result, "s")
            packnumber = get_attribute(result, "n")
            pack = XDCCPack(IrcServer("irc.rizon.net"), botname, packnumber)
            pack.set_filename(filename)
            pack.set_size(filesize)
            packs.append(pack)

        except IndexError:  # In case the line is not parseable
            pass
    return packs


def get_attribute(pack_string: str, attribute: str) -> str or int:
    """
    Parses a horriblesubs pack string for an attribute

    :param pack_string: the string to parse
    :param attribute:   the attribute to get
    :return:            the requested attribute
    """
    attribute_value = pack_string.split(attribute + ":")[1].split(",")[0]
    if attribute in ["b", "f"]:  # bot or file is encased in quotes
        return attribute_value.split("\"")[1].split("\"")[0]
    elif attribute == "s":
        return attribute_value + "M"  # Size is in Megabyte
    elif attribute == "n":
        return int(attribute_value)
    else:  # pragma: no cover
        pass
