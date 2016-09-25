"""
LICENSE:
Copyright 2015,2016 Hermann Krumrey

This file is part of toktokkie.

    toktokkie is a program that allows convenient managing of various
    local media collections, mostly focused on video.

    toktokkie is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    toktokkie is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with toktokkie.  If not, see <http://www.gnu.org/licenses/>.
LICENSE
"""

# imports
import os
import random
import shlex
import struct
import sys
import time
import irc.client
from typing import List
from puffotter.stringformatter import ForegroundColors, BackgroundColors, print_formatted_string
from toktokkie.modules.objects.ProgressStruct import ProgressStruct
from jaraco.stream import buffer


# This construct ignores all non-decodeable received strings
class IgnoreErrorsBuffer(buffer.DecodingLineBuffer):
    def handle_exception(self):
        pass
irc.client.ServerConnection.buffer_class = IgnoreErrorsBuffer
irc.client.SimpleIRCClient.buffer_class = IgnoreErrorsBuffer


class IrcLibImplementation(irc.client.SimpleIRCClient):
    """
    This class extends the SimpleIRCClient Class to download XDCC packs using the irclib library
    It is based on the tutorial scripts on the library's Github page, but strongly modified to suit the
    needs of the batch download manager.
    """

    server = ""
    """
    The server address of the server the downloader has to connect to.
    """

    bot = ""
    """
    The bot serving the requested file
    """

    pack = -1
    """
    The pack number of the file to be downloaded
    """

    destination_directory = ""
    """
    The directory to which the file should be downloaded to
    """

    nickname = ""
    """
    A nickname for the bot
    """

    progress_struct = None
    """
    A progress struct to share the download progress between threads
    """

    filename = ""
    """
    The path to the downloaded file
    """

    file = None
    """
    The downloaded file opened for writing
    """

    dcc = None
    """
    The established DCC connection to the file server bot
    """

    time_counter = int(time.time())
    """
    Keeps track of the time to control how often status updates about the download are printed to the console
    """

    common_servers = ["irc.rizon.net", "irc.criten.net", "irc.scenep2p.net", "irc.freenode.net", "irc.abjects.net"]
    """
    A list of common servers to try in case a bot does not exist on a server
    """

    server_retry_counter = 0
    """
    Counter for server retries
    """

    connection_started = False
    """
    Flag that is set to true while a connection is in progress
    """

    bot_requires_channel_join = False
    """
    Flag that gets set if the bot resides in one or more channels
    """

    joined_channel = False
    """
    Flag that gets set when the bot successfully enters a channel
    """

    download_started = False
    """
    Flag that gets set once the download starts
    """

    start_time = time.time()
    """
    Timestamp to calculate if a timeout occurred in the onping() method
    """

    verbosity_level = 0
    """
    Defines how verbose the logging will be printed to the console.
    Verbosity Level 0 prints nothing
    """

    def __init__(self, server: str, bot: str, pack: int, destination_directory: str, progress_struct: ProgressStruct,
                 file_name_override: str = None, verbosity_level: int = 0) -> None:
        """
        Constructor for the IrcLibImplementation class. It initializes the base SimpleIRCClient class
        and stores the necessary information for the download process as class variables

        :param server: The server to which the Downloader needs to connect to
        :param bot: The bot serving the file to download
        :param pack: The pack number of the file to download
        :param destination_directory: The destination directory of the downloaded file
        :param progress_struct: The progress struct to keep track of the download progress between threads
        :param file_name_override: Can be set to pre-determine the file name of the downloaded file
        :param verbosity_level: The level of verbosity to run the XDCC downloader with
        :return: None
        """
        # Initialize base class
        super().__init__()

        # Store values
        self.server = server
        self.bot = bot
        self.pack = pack
        self.destination_directory = destination_directory
        self.progress_struct = progress_struct
        self.verbosity_level = verbosity_level

        # Remove the server from common server list if it is included there
        try:
            self.common_servers.remove(server)
        except ValueError:
            pass

        # If a file name is pre-defined, set the file name to be that name.
        if file_name_override is not None:
            self.filename = os.path.join(destination_directory, file_name_override)

    def log(self, string: str, priority: int, formatting: str or List[str] = None) -> None:
        """
        Prints a string, if the verbose option is set

        :param string: the string to print
        :param priority: For which verbosity level this log should be printed
        :param formatting: optional formatting options for the string used with puffotter's string formatter
        :return: None
        """
        if self.verbosity_level >= priority:
            if formatting is None:
                print(string)
            else:
                print_formatted_string(string, formatting)

    def connect(self) -> None:
        """
        Connects to the server with a randomly generated username
        :return: None
        """
        self.nickname = "media_manager_python" + str(random.randint(0, 1000000))  # Generate random nickname
        self.log("Connecting to server " + self.server + " at port 6667 as user " + self.nickname, 2,
                 ForegroundColors.WHITE)
        super().connect(self.server, 6667, self.nickname)  # Connect to server

    def start(self) -> str:
        """
        Starts the download process and returns the file path of the downloaded file once the download completes
        :return: the path to the downloaded file
        """
        success = False
        self.log("Starting Download", 2, ForegroundColors.WHITE)
        self.connection_started = False
        while not self.connection_started:
            self.connection_started = True
            try:
                self.connect()  # Connect to server
                super().start()  # Start the download

            except ConnectionAbortedError:  # Bot not found on current server
                try:
                    self.server = self.common_servers[self.server_retry_counter]
                    self.server_retry_counter += 1
                    self.reset_state()
                    self.log("Trying different server...", 2, ForegroundColors.RED)

                except IndexError:  # Went through list of servers, could not find a match
                    raise ConnectionError("Failed to find the bot on any known server")

            except SystemExit:  # Fallback in case the self.connection.quit() call failed
                success = True
            except ConnectionError:  # Bot not found on any known server
                pass

            if success:
                self.log("Download completed Successfully", 1)
            else:
                self.log("Download did not complete successfully.", 1)

            if not self.progress_struct.single_progress == self.progress_struct.single_size:
                self.log("WARNING: Progress does not match file size", 5, ForegroundColors.LIGHT_RED)
                self.log("PROGRESS: " + str(self.progress_struct.single_progress), 5, ForegroundColors.LIGHT_GRAY)
                self.log("SIZE    : " + str(self.progress_struct.single_size), 5, ForegroundColors.LIGHT_GRAY)

            # Check that the complete file was downloaded
            if self.progress_struct.single_progress < self.progress_struct.single_size:
                self.log("Download not completed successfully, trying again", 2, ForegroundColors.RED)
                self.reset_state()

        return self.filename  # Return the file path

    def reset_state(self) -> None:
        """
        Resets the state of the downloader (deletes previously downloaded file, resets progress struct)
        :return: None
        """
        self.connection_started = False
        self.bot_requires_channel_join = False
        self.joined_channel = False
        self.download_started = False
        if os.path.isfile(self.filename):
            os.remove(self.filename)
        self.progress_struct.single_progress = 0

    def on_ping(self, connection: irc.client.ServerConnection, event: irc.client.Event) -> None:
        """
        Checks for timeouts
        :param connection: the IRC connection
        :param event: the notice event
        :return: None
        """
        if connection is None:
            pass

        current_time = time.time()
        time_delta = current_time - self.start_time
        if not self.download_started and time_delta > 120.0:
            self.log("TIMEOUT: Aborting", 1, ForegroundColors.LIGHT_RED)
            event.arguments[0] = "TIMEOUT"
            self.on_disconnect(connection, event)

    def on_welcome(self, connection: irc.client.ServerConnection, event: irc.client.Event) -> None:
        """
        Method run when the IRCClient successfully connects to a server. It sends a whois request
        to find out which channel to join

        :param connection: The IRC connection
        :param event: The event that caused this method to be run
        :return: None
        """
        # Make Pycharm happy
        if event is None:
            return
        self.log("Connection to server " + self.server + " established. Sending WHOIS command for " + self.bot, 2,
                 ForegroundColors.WHITE)
        connection.whois(self.bot)

    def on_nosuchnick(self, connection: irc.client.ServerConnection, event: irc.client.Event) -> None:
        """
        Checks if there exists a bot with the specified name on the server

        :param connection: the IRC connection
        :param event: the nosuchnick event
        :return: None
        """
        self.bot_requires_channel_join = True
        self.log("NOSUCHNICK", 2, ForegroundColors.RED)
        if connection is None:
            pass
        if event.arguments[0] == self.bot:
            connection.disconnect("Bot does not exist on server")

    def on_endofwhois(self, connection: irc.client.ServerConnection, event: irc.client.Event) -> None:
        """
        Checks the end of a WHOIS command if a channel join has occured or was even necessary
        If it was not necessary, starts the download

        :param connection: the IRC connection
        :param event: the endofwhois event
        :return: None
        """
        if not self.bot_requires_channel_join:
            event.source = self.nickname
            self.on_join(connection, event)

    def on_whoischannels(self, connection: irc.client.ServerConnection, event: irc.client.Event) -> None:
        """
        Checks the channels the bot is connected to.

        :param connection: the IRC connection
        :param event: the whois channel event
        :return: None
        """
        self.bot_requires_channel_join = True
        self.log("Got WHOIS information. Bot resides in: " + event.arguments[1], 2, ForegroundColors.WHITE)

        channels = event.arguments[1].split("#")
        channels.pop(0)

        for channel in channels:
            if not self.joined_channel:
                channel_to_join = "#" + channel.split(" ")[0]
                self.log("Joining channel " + channel_to_join, 2, ForegroundColors.WHITE)
                connection.join(channel_to_join)  # Join the channel

    def on_join(self, connection: irc.client.ServerConnection, event: irc.client.Event) -> None:
        """
        Once the IRCClient successfully joins a channel, the DCC SEND request is sent to the file serving bot

        :param connection: The IRC connection
        :param event: The event that caused this method to be run
        :return: None
        """
        if event.source.startswith(self.nickname):
            self.log("Successfully joined channel", 2, ForegroundColors.WHITE)

            # Send a private message to the bot to request the pack file (xdcc send #packnumber)
            if not self.joined_channel:
                self.log("Sending XDCC SEND request to " + self.bot, 2, ForegroundColors.WHITE)
                connection.privmsg(self.bot, "xdcc send #" + str(self.pack))
                self.joined_channel = True

    def on_ctcp(self, connection: irc.client.ServerConnection, event: irc.client.Event) -> None:
        """
        This initializes the XDCC file download, once the server is ready to send the file.

        :param connection: The IRC connection
        :param event: The event that caused this method to be run
        :return: None
        """
        self.log("ON CTCP: " + str(event.arguments), 3, ForegroundColors.BLUE)
        # Make Pycharm happy
        if connection is None or event.arguments[0] != "DCC":
            return

        # Check that the correct type of CTCP message is received
        try:
            payload = event.arguments[1]
        except IndexError:
            return
        # Parse the arguments
        parts = shlex.split(payload)
        if len(parts) > 6:
            self.log("Too many arguments: " + str(event.arguments), 3)
            return

        if len(parts) == 5:
            command, filename, peer_address, peer_port, size = parts
        else:
            command, filename, peer_address, peer_port, size, dummy = parts

        self.log("Starting Download of " + filename, 2, ForegroundColors.LIGHT_BLUE)

        if command != "SEND":  # Only react on SENDs
            return

        self.progress_struct.single_size = int(size)  # Store the file size in the progress struct

        # Set the file name, but only if it was not set previously
        if not self.filename:
            self.filename = os.path.join(self.destination_directory, os.path.basename(filename))
        else:
            # Add file extension to override-name
            extension = "." + filename.rsplit(".", 1)[1]
            if not self.filename.endswith(extension):
                self.filename += extension

        # Check if the file already exists. If it does, delete it beforehand
        if os.path.exists(self.filename):
            self.log("Deleting prevously existing file", 2, BackgroundColors.LIGHT_RED)
            os.remove(self.filename)

        self.file = open(self.filename, "wb")  # Open the file for writing
        peer_address = irc.client.ip_numstr_to_quad(peer_address)  # Calculate the bot's address
        peer_port = int(peer_port)  # Cast peer port to an integer value
        self.dcc = self.dcc_connect(peer_address, peer_port, "raw")  # Establish the DCC connection to the bot
        self.log("Established DCC connection", 2, ForegroundColors.WHITE)
        self.download_started = True

    def on_dccmsg(self, connection: irc.client.ServerConnection, event: irc.client.Event) -> None:
        """
        Run each time a new chunk of data is received while downloading

        :param connection: The IRC connection
        :param event: The event that caused this method to be run
        :return: None
        """
        # Make Pycharm happy
        if connection is None:
            return

        data = event.arguments[0]  # Get the received data
        self.file.write(data)  # and write it to file
        self.progress_struct.single_progress += len(data)  # Increase the progress struct's value

        # Print message to the console once every second
        if self.time_counter < int(time.time()):  # Check the time
            self.time_counter = int(time.time())  # Update the time counter

            # Format the string to print
            single_progress = float(self.progress_struct.single_progress) / float(self.progress_struct.single_size)
            single_progress *= 100.00
            single_progress_formatted_string = " (%.2f" % single_progress + " %)"
            progress_fraction = str(self.progress_struct.single_progress) + "/" + str(self.progress_struct.single_size)

            # Print, and line return
            if self.verbosity_level > 0:
                print(progress_fraction + single_progress_formatted_string, end="\r")

        # Communicate with the server
        self.dcc.send_bytes(struct.pack("!I", self.progress_struct.single_progress))

    def on_dcc_disconnect(self, connection: irc.client.ServerConnection, event: irc.client.Event) -> None:
        """
        Whenever the download completes, print a summary to the console and disconnect from the IRC network

        :param connection: The IRC connection
        :param event: The event that caused this method to be run
        :return: None
        """
        # Make Pycharm happy
        if connection is None or event is None:
            pass

        self.file.close()  # Close the file
        # Print a summary of the file
        self.log("Received file %s (%d bytes)." % (self.filename, self.progress_struct.single_progress), 1,
                 BackgroundColors.LIGHT_YELLOW)
        self.connection.quit()  # Close the IRC connection

        if self.connection.connected:
            self.on_disconnect(connection, event)

    # noinspection PyMethodMayBeStatic
    def on_disconnect(self, connection: irc.client.ServerConnection, event: irc.client.Event) -> None:
        """
        Stop the program when a disconnect occurs (Gets excepted by the start() method)

        :param connection: The IRC connection
        :param event: The event that caused this method to be run
        :return: None
        """
        self.log("Disconnected", 2, ForegroundColors.RED)
        # Make Pycharm happy
        if connection is None:
            pass
        if event.arguments[0] == "Bot does not exist on server":
            raise ConnectionAbortedError("Bot does not exist on server")
        if event.arguments[0] == "TIMEOUT":
            raise ConnectionError("Timeout")
        else:
            sys.exit(0)

    def on_privmsg(self, connection: irc.client.ServerConnection, event: irc.client.Event) -> None:
        """
        Logs a private message
        :param connection: the IRC connection
        :param event: the message event
        :return: None
        """
        if connection is None:
            pass
        self.log("PRIVATE MESSAGE: " + str(event.arguments), 4, ForegroundColors.YELLOW)

    def on_privnotice(self, connection: irc.client.ServerConnection, event: irc.client.Event) -> None:
        """
        Logs a private notice
        :param connection: the IRC connection
        :param event: the notice event
        :return: None
        """
        if connection is None:
            pass
        self.log("PRIVATE NOTICE: " + str(event.arguments), 4, ForegroundColors.LIGHT_YELLOW)

    def on_pubmsg(self, connection: irc.client.ServerConnection, event: irc.client.Event) -> None:
        """
        Logs a public message
        :param connection: the IRC connection
        :param event: the message event
        :return: None
        """
        if connection is None:
            pass
        self.log("PUBLIC MESSAGE: " + str(event.arguments), 4, ForegroundColors.MAGENTA)

    def on_pubnotice(self, connection: irc.client.ServerConnection, event: irc.client.Event) -> None:
        """
        Logs a public notice
        :param connection: the IRC connection
        :param event: the notice event
        :return: None
        """
        if connection is None:
            pass
        self.log("PUBLIC NOTICE: " + str(event.arguments), 4, ForegroundColors.LIGHT_MAGENTA)
