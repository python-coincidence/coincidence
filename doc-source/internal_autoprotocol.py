# stdlib
from typing import Any, List, Tuple

# 3rd party
from sphinx.application import Sphinx
from sphinx.ext.autodoc import INSTANCEATTR
from sphinx.util.inspect import safe_getattr
from sphinx_toolbox.more_autodoc.autoprotocol import ProtocolDocumenter, globally_excluded_methods
from sphinx_toolbox.utils import SphinxExtMetadata, allow_subclass_add, filter_members_warning


class CoincidenceProtocolDocumenter(ProtocolDocumenter):

	def filter_members(
			self,
			members: List[Tuple[str, Any]],
			want_all: bool,
			) -> List[Tuple[str, Any, bool]]:
		"""
		Filter the given member list.

		:param members:
		:param want_all:
		"""

		ret = []

		# process members and determine which to skip
		for (membername, member) in members:
			# if isattr is True, the member is documented as an attribute

			if safe_getattr(member, "__sphinx_mock__", False):
				# mocked module or object
				keep = False  # pragma: no cover

			elif (
					self.options.get("exclude-protocol-members", [])
					and membername in self.options["exclude-protocol-members"]
					):
				# remove members given by exclude-protocol-members
				keep = False  # pragma: no cover

			elif membername in {"_abc_impl", "_is_runtime_protocol"}:
				keep = False

			elif membername not in globally_excluded_methods:
				# Magic method you wouldn't overload, or private method.
				if membername in dir(self.object.__base__):
					keep = member is not getattr(self.object.__base__, membername)
				else:
					keep = True

			else:
				keep = False

			# give the user a chance to decide whether this member
			# should be skipped
			if self.env.app:
				# let extensions preprocess docstrings
				try:
					skip_user = self.env.app.emit_firstresult(
							"autodoc-skip-member",
							self.objtype,
							membername,
							member,
							not keep,
							self.options,
							)

					if skip_user is not None:
						keep = not skip_user

				except Exception as exc:
					filter_members_warning(member, exc)
					keep = False

			if keep:
				ret.append((membername, member, member is INSTANCEATTR))

		return ret


def setup(app: Sphinx) -> SphinxExtMetadata:
	app.setup_extension("sphinx_toolbox.more_autodoc.autoprotocol")
	allow_subclass_add(app, CoincidenceProtocolDocumenter)

	return {"parallel_read_safe": True}
