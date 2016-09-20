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
from raven import Client


"""
The metadata is stored here. It can be used by any other module in this project this way, most
notably by the setup.py file
"""

project_name = "xdcc_dl"
"""
The name of the project
"""

project_description = "An XDCC Downloader"
"""
A short description of the project
"""

version_number = "0.1"
"""
The current version of the program.
"""

development_status = "Development Status :: 1 - Planning"
"""
The current development status of the program
"""

project_url = "http://gitlab.namibsun.net/namboy94/xdcc-downloader"
"""
A URL linking to the home page of the project, in this case a
self-hosted Gitlab page
"""

download_url = "http://gitlab.namibsun.net/namboy94/xdcc-downloader/repository/archive.zip?ref=master"
"""
A URL linking to the current source zip file.
"""

author_name = "Hermann Krumrey"
"""
The name(s) of the project author(s)
"""

author_email = "hermann@krumreyh.com"
"""
The email address(es) of the project author(s)
"""

license_type = "GNU GPL3"
"""
The project's license type
"""

dependencies = ['irc', 'raven']
"""
Python Packaging Index requirements
"""

audience = "Intended Audience :: Developers"
"""
The intended audience of this software
"""

environment = "Environment :: Console"
"""
The intended environment in which the program will be used
"""

programming_language = "Programming Language :: Python"
"""
The programming language used in this project
"""

topic = "Topic :: Communications :: File Sharing"
"""
The broad subject/topic of the project
"""

language = "Natural Language :: English"
"""
The (default) language of this project
"""

compatible_os = "Operating System :: OS Independent"
"""
The Operating Systems on which the program can run
"""

license_identifier = "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
"""
The license used for this project
"""

# Sentry Configuration
sentry = Client(dsn='http://8b90175acd344261868e2054f95b6183:2bd3e783431348d1a3d9968c362de51f@85.214.124.204:9000/3',
                release=version_number)
"""
The Sentry client for logging bugs
"""