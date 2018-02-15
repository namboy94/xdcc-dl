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
import os
import sys
import argparse
from xdcc_dl.xdcc.XDCCDownloader import XDCCDownloader
from xdcc_dl.tui.XDCCDownloaderTui import XDCCDownloaderTui
from xdcc_dl.entities.XDCCPack import xdcc_packs_from_xdcc_message

try:
    from xdcc_dl.gui.XDCCDownloaderGui import start as start_gui
except ImportError:  # pragma: no cover
    start_gui = None


def main():
    """
    Starts the main method of the program

    :return: None
    """
    try:

        parser = argparse.ArgumentParser()
        parser.add_argument("message", nargs='?',
                            help="An XDCC Message. "
                                 "Supports ranges (1-100) and "
                                 "also ranges with steps (1-100,2)")
        parser.add_argument("-s", "--server",
                            help="Specifies the IRC Server. "
                                 "Defaults to irc.rizon.net")
        parser.add_argument("-d", "--destination",
                            help="Specifies the target download destination. "
                                 "Defaults to " + os.getcwd())
        parser.add_argument("-o", "--out",
                            help="Specifies the target file. "
                                 "Defaults to the pack's file name. "
                                 "When downloading multiple packs, index "
                                 "numbers will be appended to the filename")
        parser.add_argument("-u", "--username",
                            help="Specifies the username")
        parser.add_argument("-v", "--verbosity", type=int, default=1,
                            help="Specifies the verbosity of the output "
                                 "on a scale of 1-7. Default: 1")
        parser.add_argument("-g", "--gui", action="store_true",
                            help="Starts the XDCC Downloader GUI")
        parser.add_argument("-t", "--tui", action="store_true",
                            help="Starts the XDCC Downloader TUI")
        args = parser.parse_args()

        if args.message:

            destination = os.getcwd() if not args.destination \
                else args.destination

            server = "irc.rizon.net" if not args.server else args.server
            user = "random" if not args.username else args.username
            verbosity = args.verbosity

            packs = xdcc_packs_from_xdcc_message(
                args.message, destination, server
            )

            if args.out is not None:
                if len(packs) == 1:
                    packs[0].set_filename(args.out, True)
                else:
                    for i, pack in enumerate(packs):
                        pack.set_filename(args.out + "-" + str(i), True)

            downloader = XDCCDownloader(server, user, verbosity)
            results = downloader.download(packs)
            downloader.quit()

            max_length = max(map(
                lambda x: len(x.get_filepath()), results.keys()
            ))
            for result in results:
                print_result = result.get_filepath().ljust(max_length) + " - "
                print_result += results[result]
                print(print_result)

        elif args.gui:  # pragma: no cover
            if start_gui is not None:
                start_gui()
            else:
                print("Error: PyQt5 not installed")

        elif args.tui:  # pragma: no cover
            XDCCDownloaderTui().start()

        else:
            print("No arguments passed. See --help for more details")
            sys.exit(0)

    except KeyboardInterrupt:
        print("Thanks for using xdcc-dl!")


if __name__ == "__main__":  # pragma: no cover

    if sys.platform == "win32" and len(sys.argv) == 1:
        sys.argv.append("-g")
    main()
