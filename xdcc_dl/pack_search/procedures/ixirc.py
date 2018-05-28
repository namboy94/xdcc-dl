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
from bs4 import BeautifulSoup
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

    # ixIRC.com replaces spaces with + symbols for search query URLs
    split_search_term = search_phrase.split(" ")
    prepared_search_term = split_search_term[0]
    i = 1
    while i < len(split_search_term):
        prepared_search_term += "+" + split_search_term[i]
        i += 1

    base_url = "https://ixirc.com/?q=" + prepared_search_term
    content = BeautifulSoup(requests.get(base_url).text, "html.parser")
    page_analysis = content.select("h3")
    page_contents = [content]
    # This will be parsed for XDCC Packs later, along with the other pages

    # IxIRC only displays 30 results per page.
    # Which is why we need to check how many pages there are in total.
    # If 'Over' is used in the h3 section of the page,
    # it means that this is not the last page with search results.
    # It displays "Over X episodes" on all pages except the last, where
    # the exact amount of results is mentioned and the word 'Over' is omitted
    number_of_pages = 2 if "Over" in page_analysis[0].text else 1

    # Check for more pages and add their content to the page_contents list,
    # only if more than one page exists
    analysing = (number_of_pages == 2)
    while analysing:

        # The new URL specifies a page number using &pn=
        url = "https://ixirc.com/?q=" + prepared_search_term + "&pn=" + \
              str(number_of_pages - 1)
        content = BeautifulSoup(requests.get(url).text, "html.parser")
        page_contents.append(content)

        page_analysis = content.select("h3")
        if "Over" in page_analysis[0].text:
            # Found another page
            number_of_pages += 1
            continue
        else:
            # This was the last page
            analysing = False

    # Establish search results
    results = []
    for content in page_contents:
        results += get_page_results(content)

    results.sort(key=lambda x: x.packnumber)
    results.sort(key=lambda x: x.bot)
    return results


def get_page_results(page_content: BeautifulSoup) -> List[XDCCPack]:
    """
    This parses a single ixIRC page to find all search results from that page

    :param page_content: The Beautifulsoup-parsed content of the page
    :return:             A list of XDCC Packs on that page
    """
    results = []
    packs = page_content.select("td")

    # Initialize the pack variables
    file_name = ""
    bot = ""
    server = ""
    pack_number = 0
    size = ""

    # Keeps track of which column the parser is currently working on
    column_count = 0

    # Counts how often the word "ago" was used,
    # which is used to keep track of on which
    # pack we currently are. Each pack has two instances of 'ago' occurring.
    ago_count = 0

    # The process is aborted whenever an invalid pack is encountered
    aborted = False

    # Flag that lets other parts of the loop know that
    # we are moving on to the next pack
    next_element = False

    # line_part is a x,y section of the rows and columns of the website.
    # We go through it in the order Left->Right, Top->Bottom
    for line_part in packs:

        if next_element and line_part.text == "":
            # Jumps to the next not-empty element
            # if we are currently jumping to the next pack
            continue

        elif next_element and not line_part.text == "":
            # We reached a new pack, start parsing the new pack
            next_element = False

        elif not next_element and line_part.text == "":
            # Invalid pack element if a string == "" in the middle of the pack,
            # abort the pack and jump to next element
            aborted = True

        elif "ago" in line_part.text and column_count > 6:
            # Counts the number of times 'ago' is seen by the parser.
            # The last two elements of a pack both end
            # with 'ago', which makes it ideal to use as a marker
            # for when a single pack element ends.
            # This only starts counting once we got all relevant information
            # from the pack itself (column_count > 6)
            # to avoid conflicts when the substring 'ago'
            # is contained inside the file name
            ago_count += 1

        # This gets the information from the pack and stores
        # them into variables.
        # This gets skipped if it has been established that the pack is invalid
        if not aborted:
            if column_count == 0:
                # File Name
                file_name = line_part.text
            elif column_count == 1:
                # Server Address
                server = "irc." + line_part.text.lower() + ".net"
            elif column_count == 2:
                # Channel Information, not needed due to /whois IRC queries
                pass
            elif column_count == 3:
                # Bot Name
                bot = line_part.text
            elif column_count == 4:
                # Pack Number
                pack_number = int(line_part.text)
            elif column_count == 5:
                pass  # This is the 'gets' section, we don't need that
            elif column_count == 6:
                # File Size
                size = line_part.text

        # Resets state after a pack was successfully parsed,
        # and adds xdcc pack to results
        if not aborted and ago_count == 2:
            ago_count = 0
            column_count = 0
            next_element = True

            # Generate XDCCPack and append it to the list
            result = XDCCPack(IrcServer(server), bot, pack_number)
            result.set_filename(file_name)
            result.set_size(size)
            results.append(result)

        # Resets state after invalid pack
        elif aborted and ago_count == 2:
            aborted = False
            ago_count = 0
            column_count = 0
            next_element = True

        if not next_element:
            # Only increment column_count in the middle of a pack,
            # not when we jump to the next pack element
            column_count += 1

    return results
