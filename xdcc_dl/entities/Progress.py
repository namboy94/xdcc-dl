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

# imports
import time


class Progress(object):
    """
    Class that keeps track of a download progress
    """

    def __init__(self, file_amount: int, callback: callable = None) -> None:
        """
        Creates a new Progress Object with a set amount of files

        :param file_amount: the files to download
        :param callback:    A callback method called whenever the progress' state is changed.
                            The callback will be given 8 parameters:
                                1: the single progress
                                2: the single progress size
                                3: the single progress completion percentage
                                4: the total progress completion percentage
                                5: the total progress
                                6: the total progress size
                                7: the current download speed in byte/s (Based on last 0.5 seconds)
                                8: the average download speed over the entire downloading process
        """
        self.start_time = time.time()
        self.speed_counter = time.time()

        self.previous_speed = 0
        self.speed_byte_counter = 0
        self.total_bytes = 0

        self.single_progress = 0
        self.single_total = 0
        self.total_progress = 0
        self.total_total = file_amount

        self.callback = callback

    def add_single_progress(self, new_bytes: int) -> int:
        """
        Adds a given amount of bytes to the single progress.

        :param new_bytes: the bytes to add
        :return:          the new single progress
        """
        self.single_progress += new_bytes
        self.total_bytes += new_bytes

        self.handle_callback()
        return self.single_progress

    def next_file(self) -> None:
        """
        Switches to the next file to download

        :return: None
        """
        if self.total_progress < self.total_total:
            self.total_progress += 1

            if self.total_progress != self.total_total:
                self.single_progress = 0
                self.single_total = 0

    def handle_callback(self) -> None:
        """
        Handles the callback method

        :return: None
        """
        if self.callback is not None:
            self.callback(self.single_progress, self.single_total, self.get_single_progress_percentage(),
                          self.total_progress, self.total_total, self.get_total_percentage(),
                          self.calculate_current_download_speed(), self.calculate_average_download_speed())

    def calculate_current_download_speed(self) -> int:
        """
        Calculates the current download speed based on the data downloaded every 0.5 seconds

        :return: The speed in byte/s
        """
        if time.time() - self.speed_counter < 0.5:
            return self.previous_speed
        else:
            bytes_downloaded = self.total_bytes - self.speed_byte_counter
            self.speed_byte_counter = self.total_bytes

            self.previous_speed = int(bytes_downloaded / (time.time() - self.speed_counter))
            self.speed_counter = time.time()

            return self.previous_speed

    def calculate_average_download_speed(self) -> int:
        """
        Calculates the average download speed during the entire run of the progress object

        :return: The average speed in byte/s
        """
        return int(self.total_bytes / (time.time() - self.start_time))

    def set_single_progress_total(self, total: int) -> None:
        """
        Sets the total amount of bytes of the single progress

        :param total: the total progress
        :return:      None
        """
        self.single_total = total

    def set_single_progress(self, progress: int) -> None:
        """
        Sets the single progress with the new file size

        :param progress: the new file size/progress of the download
        :return:         None
        """
        self.total_bytes += progress - self.single_progress
        self.single_progress = progress

        self.handle_callback()

    def get_single_progress_percentage(self) -> float:
        """
        :return: The percentage of completion of the single progress.
        """
        try:
            return (self.single_progress / self.single_total) * 100
        except ZeroDivisionError:
            return 0.0

    def get_total_percentage(self) -> float:
        """
        :return: The percentage of total progress
        """
        if self.total_progress == self.total_total and self.total_progress != 0:
            return 100.0

        try:
            total_percentage = self.total_progress / self.total_total
            single_percentage = (self.get_single_progress_percentage() / 100)
            single_proportional_percentage = single_percentage * (1 / self.total_total)

            total_percentage += single_proportional_percentage
            return total_percentage * 100
        except ZeroDivisionError:
            return 0.0

    def get_single_progress(self) -> int:
        """
        :return: The current single progress
        """
        return self.single_progress

    def get_single_progress_total(self) -> int:
        """
        :return: The single progress
        """
        return self.single_total
