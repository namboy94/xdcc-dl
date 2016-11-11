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
import os
from xdcc_dl.metadata import PypiVariables
from setuptools import setup, find_packages


def readme():
    """
    Reads the readme file.

    :return: the readme file as a string
    """
    # noinspection PyBroadException
    try:
        # noinspection PyPackageRequirements
        import pypandoc
        with open('README.md') as f:
            # Convert markdown file to rst
            markdown = f.read()
            rst = pypandoc.convert(markdown, 'rst', format='md')
            return rst
    except:
        # If pandoc is not installed, just return the raw markdown text
        with open('README.md') as f:
            return f.read()


def find_scripts():
    """
    Returns a list of scripts in the bin directory

    :return: the list of scripts
    """
    try:
        scripts = []
        for file_name in os.listdir("bin"):
            if not file_name == "__init__.py" and os.path.isfile(os.path.join("bin", file_name)):
                scripts.append(os.path.join("bin", file_name))
        return scripts
    except OSError:
        return []

setup(name=PypiVariables.name,
      version=PypiVariables.version,
      description=PypiVariables.description,
      long_description=readme(),
      classifiers=PypiVariables.classifiers,
      url=PypiVariables.url,
      download_url=PypiVariables.download_url,
      author=PypiVariables.author,
      author_email=PypiVariables.author_email,
      license=PypiVariables.license,
      packages=find_packages(),
      install_requires=PypiVariables.install_requires,
      test_suite='nose.collector',
      tests_require=['nose'],
      scripts=find_scripts(),
      zip_safe=False)
