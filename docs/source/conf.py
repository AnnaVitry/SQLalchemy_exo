import os
import sys

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "SQLalchemy_exo"
copyright = "2026, AnnaVitry"
author = "AnnaVitry"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
sys.path.insert(0, os.path.abspath("../../"))
sys.path.insert(0, os.path.abspath("../../app"))

extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
    "myst_parser",
    "sphinxcontrib.bibtex",
]

templates_path = ["_templates"]
exclude_patterns = []

language = "fr"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_logo = "_static/img/favicon.svg"
html_title = "Documentation - Sphinx - UV - Exo SQLalchemy"
html_static_path = ["_static"]
html_theme_options = {
    "sidebar_hide_name": True,
}

# -- Configuration de la bibliographie (sphinxcontrib-bibtex) ----------------
# Spécifie les fichiers de base de données BibTeX contenant les références
# citées dans les docstrings et les guides (ex: :cite:p:`key`).
# Le fichier 'refs.bib' doit se trouver dans le dossier 'docs/source/'.
bibtex_bibfiles = ["refs.bib"]
