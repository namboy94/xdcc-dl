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
from toktokkie.modules.utils.searchengines import GenericGetter
from toktokkie.modules.utils.searchengines.NIBLGetter import NIBLGetter
from toktokkie.modules.utils.searchengines.IntelGetter import IntelGetter
from toktokkie.modules.utils.searchengines.IxIRCGetter import IxIRCGetter
from toktokkie.modules.utils.searchengines.HorribleSubsGetter import HorribleSubsGetter


class SearchEngineManager(object):
    """
    A class that manages the different kind of implemented XDCC search engines

    It offers methods to get the correct search engine class based on a string value and
    offers information on which Search engines are available
    """

    search_engines = [HorribleSubsGetter,
                      NIBLGetter,
                      IxIRCGetter,
                      IntelGetter]
    """
    The supported search engines
    """

    # noinspection PyTypeChecker
    @staticmethod
    def get_search_engine_strings() -> List[str]:
        """
        Returns search engine identifiers as strings.

        :return: A list of search engine identifier strings
        """
        # Initialize string list
        search_engine_identifiers = []

        for search_engine in SearchEngineManager.search_engines:  # Iterate over all search engines
            search_engine_identifiers.append(search_engine.get_string_identifier())  # Add to list
        return search_engine_identifiers  # and return the string list

    @staticmethod
    def get_search_engine_from_string(string_identifier) -> GenericGetter:
        """
        Takes a string identifier and searches for a search engine matching that string

        :param string_identifier: The identifier with which the Search Engine will be selected
        :return: The specified Search Engine
        """
        # This will be the variable that will be returned
        found_search_engine = None

        # Iterate over all search engines
        for search_engine in SearchEngineManager.search_engines:
            # Check if the identifier matches
            if search_engine.get_string_identifier() == string_identifier:
                # Check if another Search Engine was already found
                if found_search_engine is None:
                    # If not, set the found_search_engine variable to that search engine
                    found_search_engine = search_engine
                else:
                    # But if there was already a match, raise an Exception, since this should not happen
                    raise AssertionError("Found more than one Search Engine for unique string identifier")

        # Raise Exception when no search engine was found.
        if found_search_engine is None:
            raise AssertionError("Found no Search Engine for string identifier '" + string_identifier +
                                 "', was SearchEngineManager.get_search_engine_strings() used?")
        else:
            # If everything is OK, return the Search Engine
            return found_search_engine
