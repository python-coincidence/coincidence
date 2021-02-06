# stdlib
import sys
from collections import ChainMap, Counter, OrderedDict, defaultdict, namedtuple
from types import MappingProxyType
from typing import NamedTuple

# 3rd party
import pytest
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.stringlist import StringList
from pytest_regressions.file_regression import FileRegressionFixture

# this package
from coincidence import check_file_output, check_file_regression
from coincidence.regressions import AdvancedFileRegressionFixture


class Count(NamedTuple):
	a: int
	b: int
	c: int


Count2 = namedtuple("Count2", "a, b, c")


@pytest.mark.parametrize(
		"data",
		[
				pytest.param({'a': 1, 'b': 2, 'c': 3}, id="dict"),
				pytest.param(OrderedDict(a=1, b=2, c=3), id="OrderedDict"),
				pytest.param(Counter(a=1, b=2, c=3), id="Counter"),
				pytest.param(defaultdict(int, a=1, b=2, c=3), id="defaultdict"),
				pytest.param(Count(a=1, b=2, c=3), id="typing.NamedTuple"),
				pytest.param(Count2(a=1, b=2, c=3), id="collections.namedtuple"),
				pytest.param(['a', 1, 'b', 2, 'c', 3], id="list"),
				pytest.param(('a', 1, 'b', 2, 'c', 3), id="tuple"),
				pytest.param(MappingProxyType({'a': 1, 'b': 2, 'c': 3}), id="MappingProxyType"),
				pytest.param(ChainMap({'a': 1}, {'b': 2}, {'c': 3}), id="ChainMap"),
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


def test_check_file_output(tmp_pathplus: PathPlus, file_regression: FileRegressionFixture):
	with pytest.raises(FileNotFoundError, match="No such file or directory: '.*'"):
		check_file_output(tmp_pathplus / "file.txt", file_regression)

	(tmp_pathplus / "file.txt").write_text("Success!")
	check_file_output(tmp_pathplus / "file.txt", file_regression)

	(tmp_pathplus / "file.py").write_text("print('Success!')")
	check_file_output(tmp_pathplus / "file.py", file_regression)


def test_check_file_regression(tmp_pathplus: PathPlus, file_regression: FileRegressionFixture):
	with pytest.raises(FileNotFoundError, match="No such file or directory: '.*'"):
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


def test_advanced_file_regression_bytes(advanced_file_regression: AdvancedFileRegressionFixture):
	advanced_file_regression.check_bytes(b"Hello World\n")


def test_advanced_file_regression_output(
		tmp_pathplus: PathPlus, advanced_file_regression: AdvancedFileRegressionFixture
		):
	with pytest.raises(FileNotFoundError, match="No such file or directory: '.*'"):
		advanced_file_regression.check_file(tmp_pathplus / "file.txt")

	(tmp_pathplus / "file.txt").write_text("Success!")
	advanced_file_regression.check_file(tmp_pathplus / "file.txt")

	(tmp_pathplus / "file.py").write_text("print('Success!')")
	advanced_file_regression.check_file(tmp_pathplus / "file.py")
