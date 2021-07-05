# stdlib
import re
from typing import List, Optional, Tuple

# 3rd party
import docutils.nodes
from docutils import nodes, utils
from docutils.nodes import Node, system_message
from domdf_python_tools.paths import PathPlus
from sphinx import addnodes
from sphinx.application import Sphinx
from sphinx.transforms import SphinxTransform
from sphinx.util.docutils import SphinxRole
from sphinx.util.nodes import clean_astext
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


def visit_title(translator: LaTeXTranslator, node: nodes.title) -> None:
	parent = node.parent

	if "changelog" not in parent.attributes["classes"]:
		LaTeXTranslator.visit_title(translator, node)
		return

	if isinstance(parent, addnodes.seealso):
		# the environment already handles this
		raise nodes.SkipNode
	elif isinstance(parent, nodes.section):
		if translator.this_is_the_title:
			LaTeXTranslator.visit_title(translator, node)
			return
		else:
			short = ''
			if node.traverse(nodes.image):
				short = f'[{translator.escape(" ".join(clean_astext(node).split()))}]'

			sectionlevel = translator.sectionnames[translator.sectionlevel]
			translator.body.append(r"\phantomsection\stepcounter{section}")
			translator.body.append(
					fr"\addcontentsline{{toc}}{{{sectionlevel}}}{{\protect\numberline{{\the{sectionlevel}}}{{{node.astext()}}}}}"
					)
			translator.body.append(fr'\{sectionlevel}{short}*{{')
			translator.context.append('}\n' + translator.hypertarget_to(node.parent))
	else:
		LaTeXTranslator.visit_title(translator, node)
		return

	translator.in_title = 1


_make_id = docutils.nodes.make_id


def make_id(string):
	if re.match(r"\d.\d.\d", string):
		return string  # .replace(".", "-")
	else:
		return _make_id(string)


docutils.nodes.make_id = make_id


class ChangelogSectionTransform(SphinxTransform):
	default_priority = 500

	def apply(self, **kwargs) -> None:

		if self.env.docname != "changelog":
			return

		for node in self.document.traverse(nodes.section):
			if re.match(r"\d.\d.\d", node.children[0].astext()):
				node.attributes["classes"].append("changelog")

				for child_node in node.traverse(nodes.section):
					child_node.attributes["classes"].append("changelog")


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
	app.add_node(
			nodes.title,
			latex=(visit_title, LaTeXTranslator.depart_title),
			)

	app.add_role("del", DelRole())
	app.add_transform(ChangelogSectionTransform)
	app.connect("build-finished", replace_geq)

	return {
			"parallel_read_safe": True,
			"parallel_write_safe": True,
			}
