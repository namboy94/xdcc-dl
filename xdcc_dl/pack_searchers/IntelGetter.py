"""
LICENSE:
Copyright 2015,2016 Hermann Krumrey

This file is part of toktokkie.

    toktokkie is a program that allows convenient managing of various
    local media collections, mostly focused on video.

    toktokkie is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    toktokkie is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with toktokkie.  If not, see <http://www.gnu.org/licenses/>.
LICENSE
"""

# imports
from typing import List

import requests
from bs4 import BeautifulSoup
from toktokkie.modules.utils.searchengines.GenericGetter import GenericGetter
from toktokkie.modules.objects.XDCCPack import XDCCPack


class IntelGetter(GenericGetter):
    """
    Class that searches the xdcc pack lists from intel.haruhichan.com
    """

    # noinspection PyTypeChecker
    def search(self) -> List[XDCCPack]:
        """
        Method that conducts the xdcc pack search

        :return: the search results as a list of XDCCPack objects
        """
        split_search_term = self.search_term.split(" ")  # Splits the search term into single words

        # Generate the search string that can be inserted into intel.haruhichan.com's URL
        # to conduct a search
        # Intel Haruhichan uses %20 to separate spaces in their search query URLs
        prepared_search_term = split_search_term[0]
        i = 1
        while i < len(split_search_term):
            prepared_search_term += "%20" + split_search_term[i]
            i += 1

        # Get information from the website
        url = "http://intel.haruhichan.com/?s=" + prepared_search_term  # Generate the URL
        content = BeautifulSoup(requests.get(url).text, "html.parser")  # Parse the HTML
        packs = content.select("td")  # Only get 'td' elements from the HTML

        results = []  # List of search results (XDCCPack objects)

        i = 0  # Start at the beginning
        bot = ""
        packnumber = ""
        size = ""
        for line in packs:

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

            if i % 5 == 0:  # First Column
                bot = line.text
            elif (i - 1) % 5 == 0:  # Second Column
                packnumber = int(line.text)
            elif (i - 2) % 5 == 0:  # Third Column (Skip)
                i += 1  # Move to next 'td' element
                continue
            elif (i - 3) % 5 == 0:  # Fourth Column
                size = line.text
            elif (i - 4) % 5 == 0:  # Fifth/Last Column (Generate XDCCPack)
                filename = line.text
                server = "irc.rizon.net"
                result = XDCCPack(filename, server, bot, packnumber, size)
                results.append(result)
            i += 1  # Move to next 'td element'

        results.sort(key=lambda x: x.packnumber)
        results.sort(key=lambda x: x.bot)
        return results

    @staticmethod
    def get_string_identifier() -> str:
        """
        Returns a unique string identifier for this XDCC Search Engine

        :return: the unique string identifier for this Search Engine
        """
        return "intel.haruhichan.com"
