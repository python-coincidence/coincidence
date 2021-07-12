# stdlib
from typing import List, Optional, Tuple

# 3rd party
from docutils import nodes, utils
from docutils.nodes import Node, system_message
from domdf_python_tools.paths import PathPlus
from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxRole
from sphinx.writers.html import HTMLTranslator
from sphinx.writers.latex import LaTeXTranslator


class del_node(nodes.paragraph):
	pass


class DelRole(SphinxRole):

	def run(self) -> Tuple[List[Node], List[system_message]]:
		node = del_node(text=utils.unescape(self.text))
		node["docname"] = self.inliner.document.settings.env.docname
		node["rawtext"] = self.rawtext
		return [node], []


def html_visit_del_node(translator: HTMLTranslator, node: del_node) -> None:
	translator.body.append("<span><del>")
	translator.visit_paragraph(node)


def html_depart_del_node(translator: HTMLTranslator, node: del_node) -> None:
	translator.body.append("</del></span>")
	translator.depart_paragraph(node)


def visit_del_node_latex(translator: LaTeXTranslator, node: del_node) -> None:
	translator.body.append(r"\st{")


def depart_del_node_latex(translator: LaTeXTranslator, node: del_node) -> None:
	translator.body.append('}')


def replace_geq(app: Sphinx, exception: Optional[Exception] = None):
	if exception:
		return

	if app.builder.name.lower() != "latex":
		return

	output_file = PathPlus(app.builder.outdir) / f"{app.builder.titles[0][1]}.tex"
	output_content = output_file.read_text()
	output_content = output_content.replace('≥', r" $\geq$ ")
	output_file.write_clean(output_content)


def setup(app: Sphinx):
	app.add_node(
			del_node,
			html=(html_visit_del_node, html_depart_del_node),
			latex=(visit_del_node_latex, depart_del_node_latex),
			)

	app.add_role("del", DelRole())
	app.connect("build-finished", replace_geq)

	return {
			"parallel_read_safe": True,
			"parallel_write_safe": True,
			}
