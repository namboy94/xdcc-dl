"""
Copyright 2016-2017 Hermann Krumrey

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
"""


class Variables(object):
    """
    Class that separates variables from the other IRC/XDCC classes
    Layer -1 of the XDCC Bot
    """

    def __init__(self):
        """
        Initializes the state variables
        """
        self.user = None
        self.server = None
        self.logger = None

        self.progress = None

        self.pack_queue = []
        self.pack_states = {}

        self.joined_channels = []
