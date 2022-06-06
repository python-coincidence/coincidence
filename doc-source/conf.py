#!/usr/bin/env python3

# This file is managed by 'repo_helper'. Don't edit it directly.

# stdlib
import os
import re
import sys

# 3rd party
from sphinx_pyproject import SphinxConfig

sys.path.append('.')

config = SphinxConfig(globalns=globals())
project = config["project"]
author = config["author"]
documentation_summary = config.description

github_url = "https://github.com/{github_username}/{github_repository}".format_map(config)

rst_prolog = f""".. |pkgname| replace:: coincidence
.. |pkgname2| replace:: ``coincidence``
.. |browse_github| replace:: `Browse the GitHub Repository <{github_url}>`__
"""

slug = re.sub(r'\W+', '-', project.lower())
release = version = config.version

sphinx_builder = os.environ.get("SPHINX_BUILDER", "html").lower()
todo_include_todos = int(os.environ.get("SHOW_TODOS", 0)) and sphinx_builder != "latex"

intersphinx_mapping = {
		"python": ("https://docs.python.org/3/", None),
		"sphinx": ("https://www.sphinx-doc.org/en/stable/", None),
		"pytest": ("https://docs.pytest.org/en/stable", None),
		"pytest-regressions": ("https://pytest-regressions.readthedocs.io/en/latest/", None),
		}

html_theme_options = {"logo_only": False}

html_context = {
		"display_github": True,
		"github_user": "python-coincidence",
		"github_repo": "coincidence",
		"github_version": "master",
		"conf_py_path": "/doc-source/",
		}
htmlhelp_basename = slug

latex_documents = [("index", f'{slug}.tex', project, author, "manual")]
man_pages = [("index", slug, project, [author], 1)]
texinfo_documents = [("index", slug, project, author, slug, project, "Miscellaneous")]

toctree_plus_types = set(config["toctree_plus_types"])

autodoc_default_options = {
		"members": None,  # Include all members (methods).
		"special-members": None,
		"autosummary": None,
		"show-inheritance": None,
		"exclude-members": ','.join(config["autodoc_exclude_members"]),
		}

latex_elements = {
		"printindex": "\\begin{flushleft}\n\\printindex\n\\end{flushleft}",
		"tableofcontents": "\\pdfbookmark[0]{\\contentsname}{toc}\\sphinxtableofcontents",
		}


def setup(app):
	# 3rd party
	from sphinx_toolbox.latex import better_header_layout

	app.connect("config-inited", lambda app, config: better_header_layout(config))


nitpicky = True
needspace_amount = r"5\baselineskip"
favicons = [{
		"rel": "icon",
		"href": "https://python-coincidence.github.io/assets/coincidence.ico",
		"sizes": "48x48",
		"type": "image/vnd.microsoft.icon"
		}]
toctree_plus_types.add("fixture")
html_logo = "../coincidence.png"
latex_elements["preamble"] = "\\usepackage{soul}"
changelog_sections_numbered = False
ignore_missing_xrefs = [
		"^pytest_regressions\\.file_regression\\.FileRegressionFixture$",
		"^pytest_regressions\\.data_regression\\.DataRegressionFixture$",
		"^coincidence\\.(utils|params)\\._T$",
		"^_pytest\\.",
		]
