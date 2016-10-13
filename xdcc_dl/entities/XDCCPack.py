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
from typing import List
from xdcc_dl.entities.IrcServer import IrcServer


class XDCCPack(object):
    """
    Class that models an XDCC Pack
    """

    def __init__(self, server: IrcServer, bot: str, packnumber: int, destination: str) -> None:
        """
        Initializes an XDCC object. It contains all the necessary information for joining the correct
        IRC server and channel and sending the download request to the correct bot, then storing the
        received file in the predetermined location. If the destination is a directory, the file will be stored
        in the directory with the default file name, if not the file will be saved at the destination exactly.
        The file extension will stay as in the original filename
        """
        self.server = server
        self.bot = bot
        self.packnumber = packnumber

        if os.path.isdir(destination):
            self.directory = destination
            self.filename = ""
        else:
            self.directory = os.path.dirname(destination)
            if not self.directory:
                self.directory = os.getcwd()
            self.filename = os.path.basename(destination)

    def set_filename(self, filename: str) -> None:
        """
        Sets the filename (or only the file extension) of the target file

        :param filename: the filename as provided by the XDCC bot
        :return: None
        """
        if self.filename and len(filename.split(".")) > 1:
            extension = filename.rsplit(".", 1)[1]
            if not self.filename.endswith(extension):
                self.filename += "." + extension

        if not self.filename:
            self.filename = filename

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

    def get_request_message(self) -> str:
        """
        Generates an xdcc send message to be sent to the bot to initiate the XDCC connection

        :return: The generated message string
        """
        return "xdcc send #" + str(self.packnumber)


def xdcc_packs_from_xdcc_message(xdcc_message: str, destination: str, server: str = "irc.rizon.net") -> List[XDCCPack]:
    """
    Generates XDCC Packs from an xdcc message of the form "/msg <bot> xdcc send #<packnumber>[-<packnumber>]"

    :param xdcc_message: the XDCC message to parse
    :param destination:  the destination file or directory of the pack
    :param server:       the server to use, defaults to irc.rizon.net for simplicity's sake
    :return:             The generated XDCC Packs in a list
    """
    bot = xdcc_message.split("/msg ")[1].split(" ")[0]

    try:
        packnumber = int(xdcc_message.rsplit("#", 1)[1])
        return [XDCCPack(IrcServer(server), bot, packnumber, destination)]
    except ValueError:
        packnumbers = xdcc_message.rsplit("#", 1)[1]
        start, end = packnumbers.split("-")

        packs = []
        for pack in range(int(start), int(end) + 1):
            packs.append(XDCCPack(IrcServer(server), bot, pack, destination))
        return packs
