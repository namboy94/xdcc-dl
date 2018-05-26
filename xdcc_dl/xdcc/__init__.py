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

from typing import List
from xdcc_dl.entities.XDCCPack import XDCCPack
from xdcc_dl.xdcc.XDCCClient import XDCCCLient


def download_packs(packs: List[XDCCPack]):
    """
    Downloads a list of XDCC Packs
    :param packs: The packs to download
    :return: None
    """

    for pack in packs:
        client = XDCCCLient(pack)
        client.download()
