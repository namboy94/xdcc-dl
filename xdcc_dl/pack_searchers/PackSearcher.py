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
from typing import List
from xdcc_dl.entities.XDCCPack import XDCCPack
from xdcc_dl.pack_searchers.procedures.nibl import find_nibl_packs
from xdcc_dl.pack_searchers.procedures.ixirc import find_ixirc_packs
from xdcc_dl.pack_searchers.procedures.namibsun import find_namibsun_packs
from xdcc_dl.pack_searchers.procedures.horriblesubs import find_horriblesubs_packs
from xdcc_dl.pack_searchers.procedures.intel_haruhichan import find_intel_haruhichan_packs


class PackSearcher(object):
    """
    Class that offers various methods to search different XDCC Packlists for XDCC Packs
    """

    procedure_map = {"nibl": find_nibl_packs,
                     "ixirc": find_ixirc_packs,
                     "namibsun": find_namibsun_packs,
                     "horriblesubs": find_horriblesubs_packs,
                     "intel_haruhichan": find_intel_haruhichan_packs}

    @staticmethod
    def get_available_pack_searchers() -> List[str]:
        """
        Returns a list of available pack searchers by name

        :return: A list of the names of the pack searchers
        """
        return list(PackSearcher.procedure_map.keys())

    def __init__(self, procedures: List[str] = list(procedure_map.keys())) -> None:
        """
        Initializes the Packsearcher with a list of procedures to consider
        All procedures are used by default

        :raises:           KeyError, if an invali procedure was specified
        :param procedures: List of procedures to use during the search
        """
        self.procedures = []
        for procedure in procedures:
            self.procedures.append(self.procedure_map[procedure])

    def search(self, search_phrase: str) -> List[XDCCPack]:
        """
        Conducts the actual search for the XDCC packs

        :param search_phrase: The search phrase to use while conducting the search
        :return:              A list of search results as XDCCPack objects
        """
        results = []
        for procedure in self.procedures:
            results += procedure(search_phrase)

        for result in results:
            result.set_original_filename(result.get_filename())

        return results
