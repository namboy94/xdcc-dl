"""LICENSE
Copyright 2016-2018 Hermann Krumrey

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
from xdcc_dl import version
from setuptools import setup, find_packages


setup(
    name="xdcc_dl",
    version=version,
    description="An XDCC File Downloader based on the irclib framework",
    long_description=open("README.md").read(),
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ],
    url="https://gitlab.namibsun.net/namboy94/xdcc-dl",
    download_url="https://gitlab.namibsun.net/namboy94/xdcc-dl/"
                 "repository/archive.zip?ref=master",
    author="Hermann Krumrey",
    author_email="hermann@krumreyh.com",
    license="GNU GPL3",
    packages=find_packages(),
    install_requires=[
        "irc", "bs4", "requests", "cfscrape", "typing", "colorama"
    ],
    test_suite='nose.collector',
    tests_require=['nose'],
    scripts=list(map(lambda x: os.path.join("bin", x), os.listdir("bin"))),
    zip_safe=False
)
