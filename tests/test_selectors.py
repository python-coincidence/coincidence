# stdlib
import platform
import sys
from typing import Tuple

# 3rd party
import pytest

# this package
from coincidence.selectors import (
		max_version,
		min_version,
		not_linux,
		not_macos,
		not_pypy,
		not_windows,
		only_linux,
		only_macos,
		only_pypy,
		only_version,
		only_windows
		)


@min_version((3, 4), reason="Failure")
def test_min_version():
	pass


@max_version("4.10", reason="Failure")
def test_max_version():
	pass


@pytest.mark.parametrize(
		"py_version",
		[
				pytest.param((3, 4), marks=only_version(3.4, "Success")),
				pytest.param((3, 5), marks=only_version(3.5, "Success")),
				pytest.param((3, 6), marks=only_version(3.6, "Success")),
				pytest.param((3, 8), marks=only_version(3.8, "Success")),
				pytest.param((3, 9), marks=only_version(3.9, "Success")),
				pytest.param((3, 10), marks=only_version(3.10, "Success")),
				]
		)
def test_only_version(py_version: Tuple[int, int]):
	if sys.version_info[:2] != py_version:
		assert False  # noqa: PT015


@not_pypy("Success")
def test_not_pypy():
	if platform.python_implementation() == "PyPy":
		assert False  # noqa: PT015


@only_pypy("Success")
def test_only_pypy():
	if platform.python_implementation() != "PyPy":
		assert False  # noqa: PT015


@not_windows("Success")
def test_not_windows():
	if sys.platform == "win32":
		assert False  # noqa: PT015


@only_windows("Success")
def test_only_windows():
	if sys.platform != "win32":
		assert False  # noqa: PT015


@not_macos("Success")
def test_not_macos():
	if sys.platform == "darwin":
		assert False  # noqa: PT015


@only_macos("Success")
def test_only_macos():
	if sys.platform != "darwin":
		assert False  # noqa: PT015


@not_linux("Success")
def test_not_linux():
	if sys.platform == "linux":
		assert False  # noqa: PT015


@only_linux("Success")
def test_only_linux():
	if sys.platform != "linux":
		assert False  # noqa: PT015
