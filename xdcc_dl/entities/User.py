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

# imports
import random
import string


class User(object):
    """
    Models an IRC user
    """

    def __init__(self, username: str = "random"):
        """
        Initializes the User

        :param username: the user's username. If left empty, or the string
                         'random' is passed, a random username consisting only
                         of ASCII characters will be generated as the username.
                         An empty string will also result in a random username
        """
        if username == "random" or username == "":
            self.username = self.generate_random_username()
        else:
            self.username = username

    def get_name(self) -> str:
        """
        :return: The user's username
        """
        return self.username

    @staticmethod
    def generate_random_username(length: int = 10) -> str:
        """
        Generates a random username of given length

        :param length: The length of the username
        :return:       The random username
        """
        return "".join(random.choice(string.ascii_uppercase)
                       for _ in range(length))
