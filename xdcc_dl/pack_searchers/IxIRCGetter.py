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


class IxIRCGetter(GenericGetter):
    """
    Class that searches the xdcc pack lists from ixirc.com
    """

    # noinspection PyTypeChecker
    def search(self) -> List[XDCCPack]:
        """
        Method that conducts the xdcc pack search. This also automatically finds out the bot and channel
        via web parsing.

        :return: the search results as a list of XDCCPack objects
        """

        # Generate search URL.
        # ixIRC.com replaces spaces with + symbols.
        split_search_term = self.search_term.split(" ")
        prepared_search_term = split_search_term[0]
        i = 1
        while i < len(split_search_term):
            prepared_search_term += "+" + split_search_term[i]
            i += 1

        # Check how many pages need to be parsed:
        number_of_pages = 1  # Minimum amount of pages to parse

        # Get information from web page
        base_url = "https://ixirc.com/?q=" + prepared_search_term
        content = BeautifulSoup(requests.get(base_url).text, "html.parser")
        page_analysis = content.select("h3")  # Search all 'h3' elements of the web page

        if "Over" in page_analysis[0].text:
            # If 'Over' is used in the h3 section of the page, it means that this is not the last
            # page with search results. It displays "Over X episodes" on all pages except the last, where
            # the exact amount of results is mentioned and the word 'Over' is omitted
            number_of_pages = 2

        urls = [base_url]

        # Check for more pages and add their URLs t the urls list.
        analysing = False
        if number_of_pages == 2:
            analysing = True
        while analysing:
            # The new URL specifies a page number using &pn=
            url = "https://ixirc.com/?q=" + prepared_search_term + "&pn=" + str(number_of_pages - 1)
            urls.append(url)
            content = BeautifulSoup(requests.get(url).text, "html.parser")
            page_analysis = content.select("h3")
            if "Over" in page_analysis[0].text:
                # Found another page
                number_of_pages += 1
                continue
            else:
                # All pages found
                analysing = False

        # Establish search results
        results = []
        for url in urls:
            self.__get_page_results__(url, results)

        results.sort(key=lambda x: x.packnumber)
        results.sort(key=lambda x: x.bot)
        return results

    # noinspection PyTypeChecker
    @staticmethod
    def __get_page_results__(url: str, results: List[XDCCPack]) -> None:
        """
        This parses a single ixIRC page to find all search results from that one URL
        :param url: the URL to parse
        :param results: the list of search results to which these new results will be added to
        :return: None
        """
        # get page info with beautifulsoup
        content = BeautifulSoup(requests.get(url).text, "html.parser")
        # Get the 'td' elements of the page
        packs = content.select("td")

        # Initialize the pack variables
        file_name = ""
        bot = ""
        server = ""
        channel = ""
        pack_number = 0
        size = ""

        column_count = 0  # Keeps track of which column the parser is currently working on
        ago_count = 0  # Counts how often the word "ago" was used
        aborted = False  # Flag that sets the 'aborted' state
        next_element = False  # Flag that lets other parts of the loop know that we are moving on to the next element

        # line_part is a x,y section of the rows and columns of the website. we go through it in the order
        # Left->Right, Top->Bottom
        for line_part in packs:
            if next_element and line_part.text == "":
                # Jumps to the next not-empty element if we are currently jumping to the next pack
                continue
            elif next_element and not line_part.text == "":
                # We reached a new pack, commencing operations (Which means we start parsing the pack again)
                next_element = False
            elif not next_element and line_part.text == "":
                # Invalid pack element if a string == "" in the middle of the pack,
                # abort the pack and jump to next element
                aborted = True
            elif "ago" in line_part.text and column_count > 6:
                # Counts the number of times 'ago' is seen by the parser.
                # The last two elements of a pack both end with 'ago', which makes it ideal to use as a marker
                # For when a single pack element ends
                # This only starts counting once we got all relevant information from the pack itself
                # to avoid conflicts when the substring 'ago' is contained inside the file name
                ago_count += 1

            # This gets the information from the pack and stores them into variables
            # This gets skipped if it has been established that the pack is invalid
            if not aborted:
                if column_count == 0:
                    file_name = line_part.text
                elif column_count == 1:
                    server = line_part.text
                elif column_count == 2:
                    # channel = line_part.text  (No longer needed thanks to /whois)
                    pass
                elif column_count == 3:
                    bot = line_part.text
                elif column_count == 4:
                    pack_number = int(line_part.text)
                elif column_count == 5:
                    pass  # This is the 'gets' section, we don't need that
                elif column_count == 6:
                    size = line_part.text

            # This is called once we have reached the end of a pack
            if not aborted and ago_count == 2:
                ago_count = 0  # Reset 'ago' counter
                column_count = 0  # Reset column counter
                next_element = True  # Sets flag to communicate that a next element was found

                # Generate XDCCPack and append it to the list
                result = XDCCPack(file_name, "irc." + server + ".net", bot, pack_number, size)
                results.append(result)

            # If an invalid pack is found, this is called
            elif aborted and ago_count == 2:
                aborted = False  # Reset aborted flag
                ago_count = 0  # Reset ago count
                column_count = 0  # Reset column count
                next_element = True  # Set next_element to true to tell the loop to move on to the next pack

            if not next_element:
                # Only increment column_count in the middle of a pack, not when we jump to the next pack element
                column_count += 1

    @staticmethod
    def get_string_identifier() -> str:
        """
        Returns a unique string identifier for this XDCC Search Engine

        :return: the unique string identifier for this Search Engine
        """
        return "ixIRC.com"
