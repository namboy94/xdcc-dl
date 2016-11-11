#!/bin/env python

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

import os

qt_designer_dir = os.path.join("xdcc_dl", "gui", "qt_designer")
pyuic_dir = os.path.join("xdcc_dl", "gui", "pyuic")

for design in os.listdir(qt_designer_dir):

    if design.endswith(".ui"):

        design_file = os.path.join(qt_designer_dir, design)
        result_file = os.path.join(pyuic_dir, design.replace(".ui", ".py"))
        os.system("pyuic5 \"" + design_file + "\" > \"" + result_file + "\"")
