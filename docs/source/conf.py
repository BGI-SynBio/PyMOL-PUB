import os
import sys

sys.path.insert(0, os.path.abspath("../../"))

extensions = ["sphinx.ext.autodoc", "sphinx.ext.doctest", "sphinx.ext.todo", "sphinx.ext.coverage",
              "sphinx.ext.mathjax", "sphinx.ext.viewcode", "sphinx.ext.githubpages", "sphinx.ext.autosectionlabel"]

source_suffix = [".rst", ".md"]

# The master toctree document.
master_doc = "index"

# General information about the project.
project = "PyMOL-PUB"
# noinspection PyShadowingBuiltins
copyright = "2023, BGI-Research"
author = "Haoling Zhang"


version = "1.0"
release = "1.0"
language = "en"
exclude_patterns = []
pygments_style = "sphinx"
todo_include_todos = False
html_theme = "sphinx_rtd_theme"
html_sidebars = {"**": ["about.html", "navigation.html", "relations.html", "searchbox.html", "donate.html"]}
htmlhelp_basename = "PyMOL-PUB doc"
latex_elements = {}
latex_documents = [(master_doc, "PyMOL-PUB.tex", "PyMOL-PUB Documentation", "Haoling Zhang", "manual")]
man_pages = [(master_doc, "PyMOL-PUB", "PyMOL-PUB Documentation", [author], 1)]
texinfo_documents = [(master_doc, "PyMOL-PUB", "PyMOL-PUB Documentation",
                      author, "PyMOL-PUB", "One line description of project.", "Miscellaneous")]
napoleon_use_ivar = True
html_favicon = "_static/favicon.svg"
