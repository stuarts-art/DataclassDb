# Configuration file for the Sphinx documentation builder.
import sys
from pathlib import Path

# import dataclassdb

# version = dataclassdb.__version__
# release = dataclassdb.__version__
# del dataclassdb

sys.path.insert(0, str(Path("..", "src")))

project = "dataclassdb"
copyright = "2026, Stuart (@stuarts-art)"
author = "Stuart"

language = "en"

pygments_style = "sphinx"
nitpicky = True

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
    "sphinx_inline_tabs",
]

templates_path = ["_templates"]
exclude_patterns = []

_repo = "https://github.com/stuarts-art/DataclassDb"
extlinks = {
    "issue": (_repo + "issues/%s", "#%s"),
    "pr": (_repo + "pull/%s", "#%s"),
    "pypi": ("https://pypi.org/project/%s/", "%s"),
}

html_theme = "alabaster"
html_static_path = ["_static"]
