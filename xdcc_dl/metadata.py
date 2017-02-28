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

# pragma: no cover
from raven import Client

"""
The metadata is stored here. It can be used by any other module in this project this way, most
notably by the setup.py file
"""

# pragma: no cover
version = "2.0.0"
"""
The current version of the program
"""

# pragma: no cover
sentry_dsn = "https://3f4217fbc10a48bf8bb119c1782d8b03:58b2a299d71d4c36a277df9add7b38c3@sentry.io/110685"
"""
The DSN used for Sentry Error Logging
"""


# pragma: no cover
class SentryLogger(object):
    """
    A pre-configured Sentry client for easy error logging

    Can be overridden by unit tests to check behaviour
    """
    # pragma: no cover
    sentry = Client(dsn=sentry_dsn, release=version)
