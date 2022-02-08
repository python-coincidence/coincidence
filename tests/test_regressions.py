# stdlib
import pathlib
import sys
from collections import ChainMap, Counter, OrderedDict, defaultdict, namedtuple
from types import MappingProxyType
from typing import Dict, Mapping, NamedTuple, Sequence

# 3rd party
import pytest
import toml
from domdf_python_tools.compat import PYPY37, PYPY38
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.stringlist import StringList
from pytest_regressions.file_regression import FileRegressionFixture

# this package
from coincidence.regressions import AdvancedFileRegressionFixture, check_file_output, check_file_regression
from coincidence.selectors import not_windows


class Count(NamedTuple):
	a: int
	b: int
	c: int


Count2 = namedtuple("Count2", "a, b, c")


class DictSubclass(dict):
	pass


class TypingDictSubclass(Dict):
	pass


class CustomMapping(Mapping):

	def __init__(self, *args, **kwargs):
		self._dict = dict(*args, **kwargs)

	def __getitem__(self, item):
		return self._dict[item]

	def __iter__(self):
		yield from self._dict

	def __len__(self):
		return len(self._dict)


class CustomSequence(Sequence):

	def __init__(self, *args, **kwargs):
		self._elements = tuple(*args, **kwargs)

	def __getitem__(self, item):
		return self._elements[item]

	def __iter__(self):
		yield from self._elements

	def __len__(self):
		return len(self._elements)


some_toml = "[section]\ntable = {a = 1, b = 2, c = 3}"


@pytest.mark.parametrize(
		"data",
		[
				pytest.param({'a': 1, 'b': 2, 'c': 3}, id="dict"),
				pytest.param(DictSubclass(a=1, b=2, c=3), id="DictSubclass"),
				pytest.param(TypingDictSubclass(a=1, b=2, c=3), id="TypingDictSubclass"),
				pytest.param(CustomMapping(a=1, b=2, c=3), id="CustomMapping"),
				pytest.param(CustomSequence([1, 2, 3]), id="CustomSequence"),
				pytest.param(OrderedDict(a=1, b=2, c=3), id="OrderedDict"),
				pytest.param(Counter(a=1, b=2, c=3), id="Counter"),
				pytest.param(defaultdict(int, a=1, b=2, c=3), id="defaultdict"),
				pytest.param(Count(a=1, b=2, c=3), id="typing.NamedTuple"),
				pytest.param(Count2(a=1, b=2, c=3), id="collections.namedtuple"),
				pytest.param(['a', 1, 'b', 2, 'c', 3], id="list"),
				pytest.param(('a', 1, 'b', 2, 'c', 3), id="tuple"),
				pytest.param(MappingProxyType({'a': 1, 'b': 2, 'c': 3}), id="MappingProxyType"),
				pytest.param(ChainMap({'a': 1}, {'b': 2}, {'c': 3}), id="ChainMap"),
				pytest.param(
						OrderedDict({'a': MappingProxyType({'a': 1})}), id="Nested_OrderedDict_MappingProxyType"
						),
				pytest.param(
						OrderedDict({'a': CustomSequence([1, 2, 3])}), id="Nested_OrderedDict_CustomSequence"
						),
				pytest.param(
						CustomSequence([MappingProxyType({'a': 1})]), id="Nested_CustomSequence_MappingProxyType"
						),
				pytest.param(CustomMapping({'a': Count(a=1, b=2, c=3)}), id="Nested_CustomMapping_NamedTuple"),
				pytest.param(toml.loads(some_toml)["section"]["table"], id="Toml_InlineTableDict"),
				pytest.param(pathlib.PurePath("/foo/bar/baz"), id="pathlib_purepath"),
				pytest.param(pathlib.PurePosixPath("/foo/bar/baz"), id="pathlib_pureposixpath"),
				pytest.param(pathlib.PureWindowsPath(r"c:\foo\bar\baz"), id="pathlib_purewindowspath"),
				pytest.param(pathlib.Path("/foo/bar/baz"), id="pathlib_path"),
				pytest.param(PathPlus("/foo/bar/baz"), id="pathplus"),
				]
		)
def test_advanced_data_regression(advanced_data_regression, data):
	print(type(data))
	print(data)
	advanced_data_regression.check(data)


def test_advanced_data_regression_capsys(advanced_data_regression, capsys):
	print("Hello World")
	print("\t\tBoo!\t\t")
	print("Trailing whitespace bad        ", file=sys.stderr)
	advanced_data_regression.check(capsys.readouterr())


def test_advanced_data_regression_capsys_nested(advanced_data_regression, capsys):
	print("Hello World")
	print("\t\tBoo!\t\t")
	print("Trailing whitespace bad        ", file=sys.stderr)
	advanced_data_regression.check(OrderedDict({'a': capsys.readouterr()}))


if PYPY37 or PYPY38:
	no_such_file_pattern = r"No such file or directory: .*PathPlus\('.*'\)"
else:
	no_such_file_pattern = "No such file or directory: '.*'"


def test_check_file_output(tmp_pathplus: PathPlus, file_regression: FileRegressionFixture):

	with pytest.raises(FileNotFoundError, match=no_such_file_pattern):
		check_file_output(tmp_pathplus / "file.txt", file_regression)

	(tmp_pathplus / "file.txt").write_text("Success!")
	check_file_output(tmp_pathplus / "file.txt", file_regression)

	(tmp_pathplus / "file.py").write_text("print('Success!')")
	check_file_output(tmp_pathplus / "file.py", file_regression)


def test_check_file_regression(tmp_pathplus: PathPlus, file_regression: FileRegressionFixture):
	with pytest.raises(FileNotFoundError, match=no_such_file_pattern):
		check_file_output(tmp_pathplus / "file.txt", file_regression)

	check_file_regression("Success!\n\nThis is a test.", file_regression)

	result = StringList("Success!")
	result.blankline()
	result.blankline(ensure_single=True)
	result.append("This is a test.")

	check_file_regression(result, file_regression)


@pytest.mark.parametrize("contents", ["Hello\nWorld", "Hello World", StringList(["Hello", "World"])])
def test_advanced_file_regression(advanced_file_regression: AdvancedFileRegressionFixture, contents):
	advanced_file_regression.check(contents)


@pytest.mark.parametrize("contents", [b"hello world", ("hello world", ), [
		"hello world",
		], 12345])
def test_advanced_file_regression_bad_type(advanced_file_regression: AdvancedFileRegressionFixture, contents):
	with pytest.raises(TypeError, match="Expected text contents but received type '.*'"):
		advanced_file_regression.check(contents)


@not_windows("It's Windows")
def test_advanced_file_regression_bytes(advanced_file_regression: AdvancedFileRegressionFixture):
	advanced_file_regression.check_bytes(b"Hello World\n")


def test_advanced_file_regression_output(
		tmp_pathplus: PathPlus,
		advanced_file_regression: AdvancedFileRegressionFixture,
		):
	with pytest.raises(FileNotFoundError, match=no_such_file_pattern):
		advanced_file_regression.check_file(tmp_pathplus / "file.txt")

	(tmp_pathplus / "file.txt").write_text("Success!")
	advanced_file_regression.check_file(tmp_pathplus / "file.txt")

	(tmp_pathplus / "file.py").write_text("print('Success!')")
	advanced_file_regression.check_file(tmp_pathplus / "file.py")
