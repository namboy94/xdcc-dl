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

# imports
import os
import re
from xdcc_dl.entities.IrcServer import IrcServer


class XDCCPack(object):
    """
    Class that models an XDCC Pack
    """

    def __init__(self, server: IrcServer, bot: str, packnumber: int):
        """
        Initializes an XDCC object. It contains all the necessary information
        for joining the correct IRC server and channel and sending the
        download request to the correct bot, then storing the
        received file in the predetermined location.
        If the destination is a directory, the file will be stored
        in the directory with the default file name,
        if not the file will be saved at the destination exactly.
        The file extension will stay as in the original filename

        :param server:       The Sever to be used by the XDCC Bot
        :param bot:          The bot serving the file
        :param packnumber:   The packnumber of the desired file
        """
        self.server = server
        self.bot = bot
        self.packnumber = packnumber
        self.directory = os.getcwd()
        self.filename = ""
        self.size = 0

        self.original_filename = ""

    def is_filename_valid(self, filename: str) -> bool:
        """
        Checks if a filename is the same as the original filename,
        if one was set previously.
        This is used internally by the IRC Bot to check if a file that
        was offered to the bot actually matches the file we want to download.

        :param filename: The file name to check
        :return:         True, if the names match, or no original filename was
                         set, otherwise False
        """
        if self.original_filename != "":
            return filename == self.original_filename
        else:
            return True

    def set_filename(self, filename: str, override: bool = False):
        """
        Sets the filename (or only the file extension) of the target file

        :param filename: the filename as provided by the XDCC bot
        :param override: Overrides the current filename
        :return:         None
        """
        if self.filename and len(filename.split(".")) > 1 and not override:
            extension = filename.rsplit(".", 1)[1]
            if not self.filename.endswith(extension):
                self.filename += "." + extension

        if not self.filename or override:
            self.filename = filename

    def set_original_filename(self, filename: str):
        """
        Sets the 'original' filename,
        a.k.a the name of the actual file to download.
        This is a method that should only be used by the pack searchers
        to add filename checks during the download.

        :param filename: The original filename as found by the PackSearcher
        :return:         None
        """
        self.original_filename = filename

    def set_directory(self, directory: str):
        """
        Sets the target directory of the XDCC PAck

        :param directory: the target directory
        :return:          None
        """
        self.directory = directory

    def set_size(self, size: int):
        """
        Sets the file size of the XDCC pack

        :param size: the size of the pack
        :return:     None
        """
        self.size = size

    def get_server(self) -> IrcServer:
        """
        :return: The server
        """
        return self.server

    def get_filepath(self) -> str:
        """
        :return: The full destination file path
        """
        return os.path.join(self.directory, self.filename)

    def get_filename(self) -> str:
        """
        :return: The currently set filename
        """
        return self.filename

    def get_size(self) -> int:
        """
        :return: The currently set file size
        """
        return self.size

    def get_bot(self) -> str:
        """
        :return: The bot
        """
        return self.bot

    def get_packnumber(self) -> int:
        """
        :return: the pack number
        """
        return self.packnumber

    def get_request_message(self, full: bool = False) -> str:
        """
        Generates an xdcc send message to be sent to the bot to initiate
        the XDCC connection

        :param full: Returns the entire message string,
                     including the bot's name, as seen on packlist sites
        :return: The generated message string
        """
        if full:
            return "/msg " + self.bot + " xdcc send #" + str(self.packnumber)
        else:
            return "xdcc send #" + str(self.packnumber)

    def __str__(self) -> str:
        """
        :return: A string representation of the pack
        """
        return self.filename + " (/msg " + self.bot + " " + \
            self.get_request_message() + ")"

    def __eq__(self, other) -> bool:
        """
        Checks two objects for equality
        :param other: The other object to check against
        :return: True if the objects are equal, false otherwise
        """
        if not issubclass(type(self), type(other)):
            return False

        return self.bot == other.bot \
            and self.packnumber == other.packnumber \
            and self.server == other.server \
            and self.filename == other.filename \
            and self.directory == other.directory

    @classmethod
    def from_xdcc_message(cls, xdcc_message: str,
                          destination_directory: str = os.getcwd(),
                          server: str = "irc.rizon.net") \
            -> list:
        """
        Generates XDCC Packs from an xdcc message of the form
        "/msg <bot> xdcc send #<packnumber>[-<packnumber>]"

        :param xdcc_message: the XDCC message to parse
        :param destination_directory: the destination directory of the file
        :param server: the server to use, defaults to irc.rizon.net for
                       simplicity's sake
        :return: The generated XDCC Packs in a list
        """
        regex = r"^/msg [^ ]+ xdcc send #" \
                r"[0-9]+((,[0-9]+)*|(-[0-9]+(;[0-9]+)?)?)$"
        if not re.search(regex, xdcc_message):
            return []

        bot = xdcc_message.split("/msg ")[1].split(" ")[0]

        try:
            packnumber = xdcc_message.rsplit("#", 1)[1]
            packnumbers = packnumber.split(",")

            packs = []
            for number in packnumbers:
                xdcc_pack = XDCCPack(IrcServer(server), bot, int(number))
                xdcc_pack.set_directory(destination_directory)
                packs.append(xdcc_pack)

            return packs

        except ValueError:
            packnumbers = xdcc_message.rsplit("#", 1)[1]
            start, end = packnumbers.split("-")

            try:
                step = int(end.split(";")[1])
                end = end.split(";")[0]
            except (IndexError, ValueError):
                step = 1

            packs = []
            for pack in range(int(start), int(end) + 1, step):
                xdcc_pack = XDCCPack(IrcServer(server), bot, pack)
                xdcc_pack.set_directory(destination_directory)
                packs.append(xdcc_pack)
            return packs
