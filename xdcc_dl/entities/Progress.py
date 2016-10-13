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


class Progress(object):
    """
    Class that keeps track of a download progress
    """

    def __init__(self, file_amount: int) -> None:
        """
        Creates a new Progress Object with a set amount of files

        :param file_amount: the files to download
        """

        self.single_progress = 0
        self.single_total = 0
        self.progress = 0
        self.total = file_amount

    def add_single_progress(self, new_bytes: int) -> int:
        """
        Adds a given amount of bytes to the single progress.

        :param new_bytes: the bytes to add
        :return:          the new single progress
        """
        self.single_progress += new_bytes
        return self.single_progress

    def next_file(self) -> None:
        """
        Switches to the next file to download

        :return: None
        """
        self.progress += 1 if self.progress < self.total else self.progress
        self.single_progress = 0

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
        try:
            total_percentage = self.progress / self.total
            single_percentage = (self.get_single_progress_percentage() / 100)
            single_proportional_percentage = single_percentage * (1 / self.total)

            total_percentage += single_proportional_percentage
            return total_percentage * 100
        except ZeroDivisionError:
            return 0.0

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
        self.single_progress = progress

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
