# 3rd party
from sphinx import addnodes
from sphinx.application import Sphinx
from sphinx.locale import admonitionlabels


def visit_seealso(self, node: addnodes.seealso) -> None:
	# 	self.body.append('\n\n\\begin{description}\\item[{%s:}] \\leavevmode' % admonitionlabels['seealso'])
	self.body.append('\n\n\\sphinxstrong{%s:} ' % admonitionlabels["seealso"])


def depart_seealso(self, node: addnodes.seealso) -> None:
	# self.body.append("\\end{description}\n\n")
	self.body.append("\n\n")


def setup(app: Sphinx):
	app.add_node(addnodes.seealso, latex=(visit_seealso, depart_seealso), override=True)
