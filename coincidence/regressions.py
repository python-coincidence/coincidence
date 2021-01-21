#!/usr/bin/env python
#
#  regressions.py
"""
Regression test helpers.
"""
#
#  Copyright © 2020-2021 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#
#  Based on https://github.com/ESSS/pytest-regressions
#  Copyright (c) 2018 ESSS
#  MIT Licensed
#

# stdlib
from collections import ChainMap, OrderedDict, defaultdict
from types import MappingProxyType
from typing import Any, Counter, Dict, Mapping, Optional, Sequence, Union

# 3rd party
import pytest
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.stringlist import StringList
from domdf_python_tools.typing import PathLike
from pytest_regressions.file_regression import FileRegressionFixture
from typing_extensions import Protocol, runtime_checkable

__all__ = [
		"check_file_output",
		"check_file_regression",
		"SupportsAsDict",
		"AdvancedDataRegressionFixture",
		"advanced_data_regression"
		]

try:
	# 3rd party
	from pytest_regressions.data_regression import DataRegressionFixture

except ImportError as e:
	if not str(e).endswith("'yaml'"):
		raise

	class DataRegressionFixture:  # type: ignore
		"""
		Placeholder ``DataRegressionFixture`` for when yaml can't be imported.
		"""

		def __init__(self, *args, **kwargs):
			raise e


def check_file_regression(
		data: Union[str, StringList],
		file_regression: FileRegressionFixture,
		extension: str = ".txt",
		**kwargs,
		):
	r"""
	Check the given data against that in the reference file.

	:param data:
	:param file_regression: The file regression fixture for the test.
	:param extension: The extension of the reference file.
	:param \*\*kwargs: Additional keyword arguments passed to
		:meth:`pytest_regressions.file_regression.FileRegressionFixture.check`.
	"""

	__tracebackhide__ = True

	if isinstance(data, StringList):
		data = str(data)

	file_regression.check(data, encoding="UTF-8", extension=extension, **kwargs)

	return True


def check_file_output(
		filename: PathLike,
		file_regression: FileRegressionFixture,
		extension: Optional[str] = None,
		newline: Optional[str] = '\n',
		**kwargs,
		):
	r"""
	Check the content of the given file against the reference file.

	:param filename:
	:param file_regression: The file regression fixture for the test.
	:param extension: The extension of the reference file.
		If :py:obj:`None` the extension is determined from ``filename``.
	:param newline: Controls how universal newlines mode works. See :func:`open`.
	:param \*\*kwargs: Additional keyword arguments passed to
		:meth:`pytest_regressions.file_regression.FileRegressionFixture.check`.
	"""

	__tracebackhide__ = True

	filename = PathPlus(filename)

	data = filename.read_text(encoding="UTF-8")
	extension = extension or filename.suffix

	if extension == ".py":
		extension = "._py_"

	return check_file_regression(data, file_regression, extension, newline=newline, **kwargs)


@runtime_checkable
class SupportsAsDict(Protocol):
	"""
	:class:`typing.Protocol` for classes like :func:`collections.namedtuple` and :class:`typing.NamedTuple`
	which implement an :meth:`~._asdict` method.
	"""  # noqa: D400

	def _asdict(self) -> Dict[str, Any]:
		"""
		Return a new dict which maps field names to their corresponding values.
		"""


class AdvancedDataRegressionFixture(DataRegressionFixture):
	"""
	Subclass of :class:`~pytest_regressions.data_regression.DataRegressionFixture`
	with support for :class:`collections.OrderedDict`, :class:`collections.Counter`,
	and :func:`collections.NamedTuple`.
	"""  # noqa: D400

	def check(
			self,
			data_dict: Union[Sequence, SupportsAsDict, Mapping, MappingProxyType],
			basename: Optional[str] = None,
			fullpath: Optional[str] = None,
			):
		"""
		Checks ``data`` against a previously recorded version, or generates a new file.

		:param data_dict:

		:param basename: The basename of the file to test/record.
			If not given the name of the test is used.

		:param fullpath: The aomplete path to use as a reference file.
			This option will ignore ``datadir`` fixture when reading *expected* files,
			but will still use it to write *obtained* files.
			Useful if a reference file is located in the session data dir, for example.

		.. note::  ``basename`` and ``fullpath`` are exclusive.
		"""

		if isinstance(data_dict, (OrderedDict, Counter, defaultdict, MappingProxyType, ChainMap)):
			data_dict = dict(data_dict)
		elif isinstance(data_dict, SupportsAsDict):
			data_dict = dict(data_dict._asdict())

		super().check(data_dict, basename=basename, fullpath=fullpath)


@pytest.fixture()
def advanced_data_regression(datadir, original_datadir, request) -> AdvancedDataRegressionFixture:
	"""
	Pytest fixture for pertforming regression tests on lists, dictionaries and namedtuples.
	"""

	return AdvancedDataRegressionFixture(datadir, original_datadir, request)
