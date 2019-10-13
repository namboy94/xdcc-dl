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

from argparse import ArgumentParser
from typing import List, Optional
from xdcc_dl.entities.XDCCPack import XDCCPack


def prepare_packs(packs: List[XDCCPack], location: Optional[str]):
    """
    Prepares the output path of a list of packs based on a location string
    :param location: The location at which to save the packs.
    :param packs: The packs to prepare
    :return: None
    """
    if location is not None:
        if len(packs) == 1:
            packs[0].set_filename(location, True)
        else:
            # Generate unique names for each pack file
            for i, pack in enumerate(packs):
                pack.set_filename(location + "-" + str(i).zfill(3), True)


def add_xdcc_argparse_arguments(parser: ArgumentParser):
    """
    Adds relevant command line arguments for an argument parser for xdcc-dl
    :param parser: The parser to modify
    :return: None
    """
    parser.add_argument("-s", "--server",
                        default="irc.rizon.net",
                        help="Specifies the IRC Server. "
                             "Defaults to irc.rizon.net")
    parser.add_argument("-o", "--out",
                        help="Specifies the target file. "
                             "Defaults to the pack's file name. "
                             "When downloading multiple packs, index "
                             "numbers will be appended to the filename")
    parser.add_argument("-t", "--throttle", default=-1,
                        help="Limits the download speed of xdcc-dl. "
                             "Append K,M or G for more convenient units")
    parser.add_argument("--timeout", default=120, type=int,
                        help="Sets a timeout for starting the download")
    parser.add_argument("--fallback-channel",
                        help="Fallback channel in case a channel could not"
                             "be joined automatically using WHOIS commands")
