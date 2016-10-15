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
from toktokkie.modules.utils.searchengines.GenericGetter import GenericGetter
from toktokkie.modules.objects.XDCCPack import XDCCPack


class HorribleSubsGetter(GenericGetter):
    """
    Class that searches the xdcc pack lists from http://xdcc.horriblesubs.info/
    """

    # noinspection PyTypeChecker,PyTypeChecker
    def search(self) -> List[XDCCPack]:
        """
        Method that conducts the xdcc pack search

        :return: the search results as a list of XDCCPack objects
        """
        # Prepare the search term, nibl.co.uk uses + symbols as spaces.
        prepared_search_term = self.search_term.replace(" ", "%20")
        prepared_search_term = prepared_search_term.replace("!", "%21")

        # Get the data from the website
        url = "http://xdcc.horriblesubs.info/search.php?t=" + prepared_search_term  # Define the URL
        results = requests.get(url).text.split(";")
        packs = []

        for result in results:
            try:
                botname = self.get_attribute(result, "b")
                filename = self.get_attribute(result, "f")
                filesize = self.get_attribute(result, "s")
                packnumber = self.get_attribute(result, "n")
                pack = XDCCPack(filename, "irc.rizon.net", botname, packnumber, filesize)
                packs.append(pack)
            except IndexError:  # In case the line is not parseable
                pass

        return packs

    @staticmethod
    def get_attribute(pack_string: str, attribute: str) -> str or int:
        """
        Parses a horriblesubs pack string for an attribute

        :param pack_string: the string to parse
        :param attribute: the attribute to get
        :return: the requested attribute
        """
        attribute_value = pack_string.split(attribute + ":")[1].split(",")[0]
        if attribute in ["b", "f"]:  # bot or file is encased in quotes
            return attribute_value.split("\"")[1].split("\"")[0]
        elif attribute == "s":
            return attribute_value + "M"  # Size is in Megabyte
        elif attribute == "n":
            return int(attribute_value)

    @staticmethod
    def get_string_identifier() -> str:
        """
        Returns a unique string identifier for this XDCC Search Engine

        :return: the unique string identifier for this Search Engine
        """
        return "Horriblesubs"
