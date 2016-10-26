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
import os
import random
import argparse
from xdcc_dl.xdcc.XDCCDownloader import XDCCDownloader
from xdcc_dl.entities.XDCCPack import xdcc_packs_from_xdcc_message


def main() -> None:
    """
    Starts the main method of the program

    :return: None
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--message", help="An XDCC Message")
    parser.add_argument("-s", "--server", help="Specifies the IRC Server. Defaults to irc.rizon.net")
    parser.add_argument("-d", "--destination", help="Specifies the target download destination. Defaults to CWD")
    parser.add_argument("-u", "--username", help="Specifies the username")
    args = parser.parse_args()

    if args.message:

        destination = os.getcwd() if not args.destination else args.destination
        server = "irc.rizon.net" if not args.server else args.server
        user = str(random.random()).replace(".", "_") if not args.username else args.username

        packs = xdcc_packs_from_xdcc_message(args.message, destination, server)
        downloader = XDCCDownloader(server, user)
        downloader.download(packs)

    else:
        print("Gui Not yet implemented")


if __name__ == "__main__":
    main()
