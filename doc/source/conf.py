import sys
import os
sys.path.insert(0, os.path.abspath("../.."))
from xdcc_dl.metadata import General

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
]


templates_path = ['.templates']
source_suffix = '.rst'
master_doc = 'index'

project = 'xdcc_dl'
copyright = '2016, Hermann Krumrey'
author = 'Hermann Krumrey'

version = General.version_number
release = General.version_number

language = None
exclude_patterns = []
pygments_style = 'sphinx'

todo_include_todos = True

html_theme = 'alabaster'
html_static_path = ['.static']
htmlhelp_basename = 'xdcc_dldoc'

# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
}
latex_documents = [
    (master_doc, 'xdcc_dl.tex', 'xdcc_dl Documentation',
     'Hermann Krumrey', 'manual'),
]

man_pages = [
    (master_doc, 'xdcc_dl', 'xdcc_dl Documentation',
     [author], 1)
]

texinfo_documents = [
    (master_doc, 'xdcc_dl', 'xdcc_dl Documentation',
     author, 'xdcc_dl', 'One line description of project.',
     'Miscellaneous'),
]

epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright
epub_exclude_files = ['search.html']

intersphinx_mapping = {'https://docs.python.org/': None}

from sphinx.ext.autodoc import between


def skip(app, what, name, obj, skip, options):
    if name == "__init__":
        return False
    return skip


def setup(app):
    # Register a sphinx.ext.autodoc.between listener to ignore everything
    # between lines that contain the word IGNORE
    app.connect('autodoc-process-docstring', between('^.*LICENSE.*$', exclude=True))
    app.connect("autodoc-skip-member", skip)
    return app
