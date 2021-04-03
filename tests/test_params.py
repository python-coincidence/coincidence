# stdlib
import random
import re
from operator import itemgetter
from typing import no_type_check

# 3rd party
import pytest
from _pytest.mark import Mark, MarkDecorator, ParameterSet
from domdf_python_tools.utils import strtobool

# this package
from coincidence.params import count, param, parametrized_versions, testing_boolean_values, whitespace_perms


def test_testing_boolean_strings():
	assert isinstance(testing_boolean_values(), MarkDecorator)
	assert isinstance(testing_boolean_values().mark, Mark)
	assert "boolean_string, expected_boolean" in testing_boolean_values().mark.args
	assert testing_boolean_values().mark.args[0] == "boolean_string, expected_boolean"
	assert len(testing_boolean_values().mark.args[1]) == 28
	assert isinstance(testing_boolean_values().mark.args[1], list)
	assert isinstance(testing_boolean_values().mark.args[1][0], tuple)
	assert len(testing_boolean_values().mark.args[1][0]) == 2
	assert isinstance(testing_boolean_values().mark.args[1][0][0], bool)
	assert isinstance(testing_boolean_values().mark.args[1][0][1], bool)

	for value, expects in testing_boolean_values().mark.args[1]:
		assert strtobool(value) is expects


def test_count():
	assert isinstance(count(100), MarkDecorator)
	assert isinstance(count(100).mark, Mark)
	assert "count" in count(100).mark.args
	assert count(100).mark.args[0] == "count"
	assert count(100).mark.args[1] == range(0, 100)

	assert count(10).mark.args[1] == range(0, 10)
	assert count(10, 5).mark.args[1] == range(5, 10)  # order of count is "stop, start, step"
	assert count(10, 5, 2).mark.args[1] == range(5, 10, 2)  # order of count is "stop, start, step"


def test_whitespace_perms():
	random.seed(1234)

	assert isinstance(whitespace_perms(), MarkDecorator)
	assert isinstance(whitespace_perms().mark, Mark)
	assert "char" in whitespace_perms().mark.args
	assert whitespace_perms().mark.args[0] == "char"
	assert len(whitespace_perms().mark.args[1]) == 20
	assert len(whitespace_perms(1).mark.args[1]) == 41
	assert len(whitespace_perms(0.1).mark.args[1]) == 4

	assert isinstance(whitespace_perms(0.1).mark.args[1], list)
	assert isinstance(whitespace_perms(0.1).mark.args[1][0], str)

	assert whitespace_perms(0.1).mark.args[1] == ["\n\t\r", "\r\t", "\t \n", "\n\r"]

	for string in whitespace_perms().mark.args[1]:
		assert re.match(r"^\s*$", string)


def test_param():
	assert param("6*9", 42, marks=pytest.mark.xfail).id is None
	assert param("2**2", 4, idx=0).id == "2**2"
	assert param("3**2", 9, id="3^2").id == "3^2"
	assert param("sqrt(9)", 3, key=itemgetter(0)).id == "sqrt(9)"

	with pytest.raises(ValueError, match="'id', 'idx' and 'key' are mutually exclusive."):
		param("sqrt(9)", 3, id="√9", key=itemgetter(0))  # type: ignore

	with pytest.raises(ValueError, match="'id', 'idx' and 'key' are mutually exclusive."):
		param("sqrt(9)", 3, id="√9", idx=0)  # type: ignore

	with pytest.raises(ValueError, match="'id', 'idx' and 'key' are mutually exclusive."):
		param("sqrt(9)", 3, idx=0, key=itemgetter(0))  # type: ignore

	with pytest.raises(ValueError, match="'id', 'idx' and 'key' are mutually exclusive."):
		param("sqrt(9)", 3, id="√9", idx=0, key=itemgetter(0))  # type: ignore


@no_type_check
def test_parametrized_versions():
	versions = parametrized_versions(3.6, 3.7, 3.8, reasons="Output differs on each version.")
	assert len(versions) == 3
	assert all(isinstance(v, ParameterSet) for v in versions)

	assert versions[0].values == ("3.6", )
	assert versions[1].values == ("3.7", )
	assert versions[2].values == ("3.8", )

	assert versions[0].marks[0].mark.name == "skipif"
	assert versions[1].marks[0].mark.name == "skipif"
	assert versions[2].marks[0].mark.name == "skipif"

	assert versions[0].marks[0].kwargs["reason"] == "Output differs on each version."
	assert versions[1].marks[0].kwargs["reason"] == "Output differs on each version."
	assert versions[2].marks[0].kwargs["reason"] == "Output differs on each version."

	assert all(len(v.marks) == 1 for v in versions)


@no_type_check
def test_parametrized_versions_list():
	versions = parametrized_versions(
			"3.6",
			(3, 7),
			3.9,
			reasons=["Output differs on each version.", "Output differs on Python 3.7."],
			)

	assert len(versions) == 3
	assert all(isinstance(v, ParameterSet) for v in versions)

	assert versions[0].values == ("3.6", )
	assert versions[1].values == ("3.7", )
	assert versions[2].values == ("3.9", )

	assert versions[0].marks[0].mark.name == "skipif"
	assert versions[1].marks[0].mark.name == "skipif"
	assert versions[2].marks[0].mark.name == "skipif"

	assert versions[0].marks[0].kwargs["reason"] == "Output differs on each version."
	assert versions[1].marks[0].kwargs["reason"] == "Output differs on Python 3.7."
	assert versions[2].marks[0].kwargs["reason"] == "Not needed on Python v3.9.0."

	assert all(len(v.marks) == 1 for v in versions)
