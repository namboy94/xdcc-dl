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

from enum import Enum
from typing import List, Set
from xdcc_dl.entities.XDCCPack import XDCCPack
from xdcc_dl.pack_search.procedures.nibl import find_nibl_packs
from xdcc_dl.pack_search.procedures.ixirc import find_ixirc_packs
from xdcc_dl.pack_search.procedures.horriblesubs import find_horriblesubs_packs


class SearchEngine:
    """
    An XDCC Pack Search Engine
    """

    def __init__(self, name: str, procedure: callable):
        """
        Initializes the Search Engine
        :param name: The name of the search engine
        :param procedure: A function that performs the XDCC pack search
        """
        self.name = name
        self._procedure = procedure

    def search(self, term: str) -> List[XDCCPack]:
        """
        Searches for packs that match the provided term
        :param term: The term to search for
        :return: A list of XDCC Packs
        """
        return self._procedure(term)


class SearchEngineType(Enum):
    """
    The different implemented search engines
    """

    HORRIBLESUBS = SearchEngine("Horriblesubs", find_horriblesubs_packs)
    NIBL = SearchEngine("Nibl", find_nibl_packs)
    IXIRC = SearchEngine("iXirc", find_ixirc_packs)

    @classmethod
    def choices(cls, lower: bool = True) -> Set[str]:
        """
        Provides a set of strings that represent the possible search engine
        choices.
        :param lower: Provides lower-case names of the search engine types
        :return: The set of choices
        """
        choices = []
        for choice in cls:
            name = choice.value.name.lower() if lower else choice.value.name
            choices.append(name)
        return set(choices)

    @classmethod
    def resolve(cls, name: str) -> SearchEngine or None:
        """
        Resolves a string identifier of a search engine and provides
        the correct search engine
        :param name: The name of the search engine
        :return: The search engine object or None if no match was found
        """
        for choice in cls:
            if choice.value.name.lower() == name.lower():
                return choice.value
        return None
