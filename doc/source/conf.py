#!/usr/bin/env python3

import os
import sys
# noinspection PyPackageRequirements
import sphinx_rtd_theme
# noinspection PyPackageRequirements
from sphinx.ext.autodoc import between

version_number = ""
sys.path.insert(0, os.path.abspath("../.."))
exec("from xdcc_dl import version as version_number")

extensions = [
    'sphinx.ext.autodoc',
]

templates_path = ['.templates']
source_suffix = '.rst'
master_doc = 'index'

# noinspection PyShadowingBuiltins
copyright = '2016, Hermann Krumrey'
author = 'Hermann Krumrey'
project = 'xdcc-dl'

version = version_number
release = version_number

language = None
exclude_patterns = []
pygments_style = 'sphinx'
todo_include_todos = False

# HTML Config
html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_static_path = ['.static']
htmlhelp_basename = 'xdcc-dl-doc'

# Latex Hack to circumvent 'Too deeply nested' error
latex_elements = {
    'maxlistdepth': '7',
}

latex_documents = [
    (master_doc, 'xdcc-dl.tex', 'xdcc-dl Documentation',
     'Hermann Krumrey', 'manual'),
]

# Man Pages
man_pages = [
    (master_doc, 'xdcc-dl', 'xdcc-dl Documentation',
     [author], 1)
]

# Tex
texinfo_documents = [
    (master_doc, 'xdcc-dl', 'xdcc-dl Documentation',
     author, 'xdcc-dl', 'An XDCC Downloader bot',
     'Miscellaneous'),
]

# Epub
epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright
epub_exclude_files = ['search.html']

intersphinx_mapping = {'https://docs.python.org/': None}


def setup(app):
    """
    Registers an autodoc between listener to igore License texts

    :param app: The sphinx app
    :return:    None
    """
    app.connect('autodoc-process-docstring',
                between('^.*LICENSE.*$', exclude=True))
    app.connect("autodoc-skip-member",
                lambda a, b, name, d, skipper, f:
                False if name == "__init__" else skipper)
    return app
