#!/usr/bin/env python3

import os
import sys
sys.path.insert(0, os.path.abspath("../.."))
from xdcc_dl.metadata import General
from sphinx.ext.autodoc import between

extensions = [
    'sphinx.ext.autodoc',
]


templates_path = ['.templates']
source_suffix = '.rst'
master_doc = 'index'

# noinspection PyShadowingBuiltins
copyright = '2016, Hermann Krumrey'
author = 'Hermann Krumrey'
project = 'xdcc-downloader'

version = General.version_number
release = General.version_number
language = None


exclude_patterns = []
pygments_style = 'sphinx'
todo_include_todos = False

html_theme = 'alabaster'
html_static_path = ['.static']
htmlhelp_basename = 'xdcc-downloader-doc'


latex_elements = {
}
latex_documents = [
    (master_doc, 'xdcc-downloader.tex', 'xdcc-downloader Documentation',
     'Hermann Krumrey', 'manual'),
]

man_pages = [
    (master_doc, 'xdcc-downloader', 'xdcc-downloader Documentation',
     [author], 1)
]

texinfo_documents = [
    (master_doc, 'xdcc-downloader', 'xdcc-downloader Documentation',
     author, 'xdcc-downloader', 'An XDCC Downloader bot',
     'Miscellaneous'),
]

epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright
epub_exclude_files = ['search.html']

intersphinx_mapping = {'https://docs.python.org/': None}


def skip(app, what, name, obj, skipper, options):
    str(app)
    str(what)
    str(obj)
    str(options)
    if name == "__init__":
        return False
    return skipper


def setup(app):
    # Register a sphinx.ext.autodoc.between listener to ignore everything
    # between lines that contain the word IGNORE
    app.connect('autodoc-process-docstring', between('^.*LICENSE.*$', exclude=True))
    app.connect("autodoc-skip-member", skip)
    return app
