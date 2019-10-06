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

import sys
import logging
from typing import List, Optional
from xdcc_dl.logging import Logger
from xdcc_dl.entities.XDCCPack import XDCCPack
from xdcc_dl.xdcc.XDCCClient import XDCCClient
from puffotter.units import byte_string_to_byte_count


def set_throttle_value(throttle_string: str):
    """
    Sets the throttle value of the XDCC Client globally based on a string in
    the form <Bytes><|k|m|g> (kilo, mega, giga)
    :param throttle_string: The string to parse
    :return: None
    """
    try:
        if throttle_string is not None:
            limit = byte_string_to_byte_count(throttle_string)
            XDCCClient.download_limit = limit
    except ValueError:
        print("Invalid throttle value")
        sys.exit(1)


def set_logging_level(quiet: bool, verbose: bool, debug: bool, silent: bool):
    """
    Sets the logging level based on a combination of flags
    If all flags are False, the logging level will be set to WARNING
    :param quiet: If set to True, will set logging to ERROR
    :param verbose: If set to True, will set logging to INFO
    :param debug: If set to True, will set logging to DEBUG
    :param silent: If set to True, will disable ALL printing
    :return: None
    """
    if silent:
        Logger.logging_level = -1
    elif quiet:
        Logger.logging_level = logging.ERROR
    elif verbose:
        Logger.logging_level = logging.INFO
    elif debug:
        Logger.logging_level = logging.DEBUG
    else:
        Logger.logging_level = logging.WARNING


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
