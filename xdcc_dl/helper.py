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

import sys
from xdcc_dl.xdcc.XDCCClient import XDCCCLient


def set_throttle_value(throttle_string: str):
    """
    Sets the throttle value of the XDCC Client globally based on a string in
    the form <Bytes><|k|m|g> (kilo, mega, giga)
    :param throttle_string: The string to parse
    :return: None
    """
    try:
        if throttle_string is not None:
            multiplier = 1
            units = {"k": 1000, "m": 1000000, "g": 1000000000}
            throttle_num = ""
            for i, char in enumerate(throttle_string):
                if char.isdigit():
                    throttle_num += char
                else:
                    if len(throttle_string) - 1 != i:
                        raise KeyError
                    else:
                        multiplier = units[char.lower()]
            limit = multiplier * int(throttle_num)
            XDCCCLient.download_limit = limit
    except KeyError:
        print("Invalid throttle value")
        sys.exit(1)
