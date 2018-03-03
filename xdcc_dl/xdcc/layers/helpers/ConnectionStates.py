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

# imports
import time


class ConnectionStates(object):
    """
    Class that separates state variables from the other IRC/XDCC classes
    Layer -1 of the XDCC Bot

    All of these variables should be considered obsolete for each XDCC pack
    """

    def __init__(self):
        """
        Initializes the state variables
        """
        # Connection
        self.connected_to_server = False
        self.channel_joined = False
        self.channel_join_required = False

        # Download
        self.already_requested = False
        self.download_started = False
        self.dcc_resume_requested = False
        self.already_downloaded = False

        # Download File Specific
        self.current_pack = None
        self.file = None
        self.dcc_connection = None
        self.peer_address = None
        self.peer_port = None
        self.filesize = None

        # Stats
        self.start_time = time.time()

        # Monitoring
        self.monitor_thread = None
        self.last_dcc_data_timestamp = 0

    def reset_connection_state(self):
        """
        Resets all connection state variables

        :return: None
        """
        # Connection
        self.connected_to_server = False
        self.channel_joined = False
        self.channel_join_required = False

        # Download
        self.already_requested = False
        self.download_started = False
        self.dcc_resume_requested = False
        self.already_downloaded = False

        # Download File Specific
        self.current_pack = None
        self.file = None
        self.dcc_connection = None
        self.peer_address = None
        self.peer_port = None
        self.filesize = None

        # Stats
        self.start_time = time.time()

        # Monitoring
        self.monitor_thread = None
        self.last_dcc_data_timestamp = 0
