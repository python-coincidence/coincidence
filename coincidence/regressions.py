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
import collections
from collections import ChainMap, Counter, OrderedDict, defaultdict
from contextlib import suppress
from functools import partial
from types import MappingProxyType
from typing import Any, Callable, Dict, Mapping, Optional, Sequence, Type, TypeVar, Union, cast

# 3rd party
import pytest
from _pytest.capture import CaptureResult  # nodep
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.stringlist import StringList
from domdf_python_tools.typing import PathLike
from pytest_regressions.common import check_text_files, perform_regression_check
from pytest_regressions.file_regression import FileRegressionFixture
from typing_extensions import Protocol, runtime_checkable

__all__ = [
		"check_file_output",
		"check_file_regression",
		"SupportsAsDict",
		"AdvancedDataRegressionFixture",
		"advanced_data_regression",
		"AdvancedFileRegressionFixture",
		"advanced_file_regression",
		]

_C = TypeVar("_C", bound=Callable)

try:
	# 3rd party
	from pytest_regressions.data_regression import DataRegressionFixture, RegressionYamlDumper

except ImportError as e:  # pragma: no cover
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

	.. seealso:: :meth:`.AdvancedFileRegression.check`
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
	Check the content of the given text file against the reference file.

	:param filename:
	:param file_regression: The file regression fixture for the test.
	:param extension: The extension of the reference file.
		If :py:obj:`None` the extension is determined from ``filename``.
	:param newline: Controls how universal newlines mode works. See :func:`open`.
	:param \*\*kwargs: Additional keyword arguments passed to
		:meth:`pytest_regressions.file_regression.FileRegressionFixture.check`.

	.. seealso:: :meth:`.AdvancedFileRegression.check_file`
	"""

	filename = PathPlus(filename)

	data = filename.read_text(encoding="UTF-8")
	extension = extension or filename.suffix

	if extension == ".py":
		extension = "._py_"

	__tracebackhide__ = True

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
	Subclass of :class:`~pytest_regressions.data_regression.DataRegressionFixture` with support for additional types.

	The following types and their subclasses are supported:

	* :class:`collections.abc.Mapping`, :class:`typing.Mapping` (including :class:`dict` and :class:`typing.Dict`)
	* :class:`collections.abc.Sequence`, :class:`typing.Sequence` (including :class:`list`, :class:`typing.Tuple` etc.)
	* :class:`collections.OrderedDict`, :class:`typing.OrderedDict`
	* :class:`collections.Counter`, :class:`typing.Counter`
	* :class:`types.MappingProxyType` (cannot be subclassed)
	* :class:`_pytest.capture.CaptureResult` (the type of :meth:`capsys.readouterr() <pytest.CaptureFixture.readouterr>`)
	* Any type which implements the :protocol:`SupportsAsDict` protocol (including :class:`collections.namedtuple` and :class:`typing.NamedTuple`)
	"""

	def check(
			self,
			data_dict: Union[Sequence, SupportsAsDict, Mapping, MappingProxyType, CaptureResult],
			basename: Optional[str] = None,
			fullpath: Optional[str] = None,
			):
		"""
		Checks ``data`` against a previously recorded version, or generates a new file.

		:param data_dict:

		:param basename: The basename of the file to test/record.
			If not given the name of the test is used.

		:param fullpath: The complete path to use as a reference file.
			This option will ignore ``datadir`` fixture when reading *expected* files,
			but will still use it to write *obtained* files.
			Useful if a reference file is located in the session data dir, for example.

		.. note::  ``basename`` and ``fullpath`` are exclusive.
		"""

		if isinstance(data_dict, (Mapping, OrderedDict, Counter, defaultdict, MappingProxyType, ChainMap)):
			data_dict = dict(data_dict)
		elif isinstance(data_dict, SupportsAsDict):
			data_dict = dict(data_dict._asdict())
		elif isinstance(data_dict, CaptureResult):
			data_dict = dict(out=data_dict.out.splitlines(), err=data_dict.err.splitlines())
		elif isinstance(data_dict, Sequence):
			data_dict = list(data_dict)

		__tracebackhide__ = True

		super().check(data_dict, basename=basename, fullpath=fullpath)


def _representer_for(*data_type: Type):

	def deco(representer_fn: _C) -> _C:
		for dtype in data_type:
			RegressionYamlDumper.add_custom_yaml_representer(dtype, representer_fn)

		return representer_fn

	return deco


@_representer_for(
		collections.abc.Mapping,
		collections.OrderedDict,
		collections.Counter,
		collections.defaultdict,
		MappingProxyType,
		)
def _represent_mappings(dumper: RegressionYamlDumper, data):
	data = dict(data)
	return dumper.represent_data(data)


@_representer_for(collections.abc.Sequence, tuple)
def _represent_sequences(dumper: RegressionYamlDumper, data):
	if isinstance(data, SupportsAsDict):
		data = dict(data._asdict())
	else:
		data = list(data)

	return dumper.represent_data(data)


@_representer_for(CaptureResult)
def _represent_captureresult(dumper: RegressionYamlDumper, data):
	data = dict(out=data.out.splitlines(), err=data.err.splitlines())
	return dumper.represent_data(data)


with suppress(TypeError):
	# 3rd party
	import toml
	_representer_for(toml.decoder.InlineTableDict)(_represent_mappings)  # type: ignore


@pytest.fixture()
def advanced_data_regression(datadir, original_datadir, request) -> AdvancedDataRegressionFixture:
	"""
	Pytest fixture for performing regression tests on lists, dictionaries and namedtuples.
	"""

	return AdvancedDataRegressionFixture(datadir, original_datadir, request)


class AdvancedFileRegressionFixture(FileRegressionFixture):
	"""
	Subclass of :class:`~pytest_regressions.file_regression.FileRegressionFixture`
	with UTF-8 by default and some extra methods.

	.. versionadded:: 0.2.0
	"""  # noqa: D400

	def check(  # type: ignore
		self,
		contents: Union[str, StringList],
		encoding: Optional[str] = "UTF-8",
		extension: str = ".txt",
		newline: Optional[str] = None,
		basename: Optional[str] = None,
		fullpath: Optional[str] = None,
		binary: bool = False,
		obtained_filename: Optional[str] = None,
		check_fn: Optional[Callable[[Any, Any], Any]] = None,
		):
		r"""
		Checks the contents against a previously recorded version, or generates a new file.

		:param contents:
		:param extension: The extension of the reference file.
		:param \*\*kwargs: Additional keyword arguments passed to
			:meth:`pytest_regressions.file_regression.FileRegressionFixture.check`.

		.. seealso:: :meth:`~.check_file_regression`
		"""

		__tracebackhide__ = True

		if isinstance(contents, StringList):
			contents = str(contents)
		elif not isinstance(contents, str):
			raise TypeError(f"Expected text contents but received type {type(contents).__name__!r}")

		if check_fn is None:
			check_fn = partial(check_text_files, encoding="UTF-8")

		def dump_fn(filename):
			PathPlus(filename, newline=newline).write_clean(contents)  # type: ignore

		perform_regression_check(
				datadir=self.datadir,
				original_datadir=self.original_datadir,
				request=self.request,
				check_fn=check_fn,
				dump_fn=dump_fn,
				extension=extension,
				basename=basename,
				fullpath=fullpath,
				force_regen=self.force_regen,
				obtained_filename=obtained_filename,
				)

	def check_bytes(self, contents: bytes, **kwargs):  # pragma: no cover (Windows)
		r"""
		Checks the bytes contents against a previously recorded version, or generates a new file.

		:param contents:
		:param \*\*kwargs: Additional keyword arguments passed to
			:meth:`pytest_regressions.file_regression.FileRegressionFixture.check`.
		"""

		__tracebackhide__ = True
		super().check(contents, binary=True, **kwargs)

	def check_file(
			self,
			filename: PathLike,
			extension: Optional[str] = None,
			newline: Optional[str] = '\n',
			**kwargs,
			):
		r"""
		Check the content of the given text file against the reference file.

		:param filename:
		:param extension: The extension of the reference file.
			If :py:obj:`None` the extension is determined from ``filename``.
		:param newline: Controls how universal newlines mode works. See :func:`open`.
		:param \*\*kwargs: Additional keyword arguments passed to
			:meth:`pytest_regressions.file_regression.FileRegressionFixture.check`.

		.. seealso:: :meth:`~.check_file_output`
		"""

		filename = PathPlus(filename)

		data = filename.read_text(encoding="UTF-8")
		extension = extension or filename.suffix

		if extension == ".py":
			extension = "._py_"

		__tracebackhide__ = True

		return self.check(data, extension=extension, newline=newline, **kwargs)


@pytest.fixture()
def advanced_file_regression(datadir, original_datadir, request) -> AdvancedFileRegressionFixture:
	"""
	Pytest fixture for performing regression tests on strings, bytes and files.

	.. versionadded:: 0.2.0
	"""

	return AdvancedFileRegressionFixture(datadir, original_datadir, request)
