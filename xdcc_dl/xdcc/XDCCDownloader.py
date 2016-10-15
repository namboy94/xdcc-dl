"""
LICENSE:
Copyright 2016 Hermann Krumrey

This file is part of xdcc_dl.

    xdcc_dl is a program that allows downloading files via hte XDCC
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

from xdcc_dl.entities import XDCCPack
from xdcc_dl.entities.Progress import Progress
from xdcc_dl.entities.User import User
from xdcc_dl.logging.Logger import Logger
from xdcc_dl.xdcc.layers.xdcc.DownloadHandler import DownloadHandler


class XDCCDownloader(DownloadHandler):
    """
    The XDCC Downloader that combines the capabilities of all XDCC Layers to offer a stable
    interface to download XDCC Packs
    """

    def __init__(self, packs: List[XDCCPack], user: User, logger: Logger, progress: Progress):
        """
        Initializes the XDCC Downloader with
        :param packs:
        :param user:
        :param logger:
        :param progress:
        """