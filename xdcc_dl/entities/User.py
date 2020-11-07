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
import names
import random


class User(object):
    """
    Models an IRC user
    """

    def __init__(self, username: str = "random"):
        """
        Initializes the User

        :param username: the user's username. If left empty, or the string
                         'random' is passed, a random username is generated
                         using the names package.
                         An empty string will also result in a random username
        """
        if username == "random" or username == "":
            self.username = \
                names.get_first_name() + \
                names.get_last_name() + \
                str(random.randint(10, 100))
        else:
            self.username = username

    def get_name(self) -> str:
        """
        :return: The user's username
        """
        return self.username
