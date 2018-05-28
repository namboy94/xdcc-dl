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


class InvalidCTCPException(Exception):
    """
    Exception thrown when an invalid CTCP DCC message type is received
    """
    pass


class AlreadyDownloadedException(Exception):
    """
    Exception thrown when a file was already downloaded
    """
    pass


class DownloadCompleted(Exception):
    """
    Exception thrown once the download has been completed
    """
    pass


class DownloadIncomplete(Exception):
    """
    Exception thrown if a download did not complete
    """
    pass
