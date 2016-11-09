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


def find_intel_haruhichan_packs(search_phrase: str) -> List[XDCCPack]:
    """
    Searches for XDCC Packs matching the specified search string on intel.haruhichan.com

    :param search_phrase: The search phrase to search for
    :return:              The list of found XDCC Packs
    """

    if not search_phrase:
        return []

    # Generate the search string that can be inserted into intel.haruhichan.com's URL to conduct a search
    # Intel Haruhichan uses %20 to separate spaces in their search query URLs
    split_search_term = search_phrase.split(" ")
    prepared_search_term = split_search_term[0]
    i = 1
    while i < len(split_search_term):
        prepared_search_term += "%20" + split_search_term[i]
        i += 1

    url = "http://intel.haruhichan.com/?s=" + prepared_search_term
    content = BeautifulSoup(requests.get(url).text, "html.parser")
    packs = content.select("td")

    results = []

    bot = ""
    packnumber = ""
    size = ""

    for i, line in enumerate(packs):

        # Explanation how this works:
        # Every fifth 'td' element is the start of a new search result. They go in order:
        #       1. Bot Name
        #       2. Pack Number
        #       3. Requests (Not used)
        #       4. File Size
        #       5. File Name
        #
        # This means, that we check with modulo 5 at which td element we currently are, and increment i
        # after every loop.
        # If we are at the fifth element, we have all the information we need to generate an XDCCPack

        if i % 5 == 0:
            bot = line.text
        elif (i - 1) % 5 == 0:
            packnumber = int(line.text)
        elif (i - 2) % 5 == 0:
            pass    # Skip the 'requests' section
        elif (i - 3) % 5 == 0:
            size = line.text
        else:
            result = XDCCPack(IrcServer("irc.rizon.net"), bot, packnumber)
            result.set_size(size)
            result.set_filename(line.text)
            results.append(result)

    results.sort(key=lambda x: x.packnumber)
    results.sort(key=lambda x: x.bot)
    return results
