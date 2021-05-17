#!/usr/bin/env python
#
#  fixtures.py
r"""
Pytest fixtures.

To enable the fixtures add the following to ``conftest.py`` in your test directory:

.. code-block:: python

	pytest_plugins = ("coincidence", )

See `the pytest documentation`_ for more information.

.. _the pytest documentation: https://pytest.org/en/latest/how-to/plugins.html
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

# stdlib
import datetime
import os
from pathlib import Path

# 3rd party
import pytest
from domdf_python_tools.paths import PathPlus

# this package
from coincidence.utils import with_fixed_datetime

__import__("pytest_datadir")

__all__ = ["fixed_datetime", "original_datadir", "tmp_pathplus", "path_separator"]


@pytest.fixture()
def tmp_pathplus(tmp_path: Path) -> PathPlus:
	"""
	Pytest fixture which returns a temporary directory in the form of a
	:class:`~domdf_python_tools.paths.PathPlus` object.

	The directory is unique to each test function invocation,
	created as a sub directory of the base temporary directory.

	Use it as follows:

	.. code-block:: python

		pytest_plugins = ("coincidence", )

		def test_something(tmp_pathplus: PathPlus):
			assert True
	"""  # noqa: D400

	return PathPlus(tmp_path)


@pytest.fixture()
def original_datadir(request) -> Path:  # noqa: D103
	# Work around pycharm confusing datadir with test file.
	return PathPlus(os.path.splitext(request.module.__file__)[0] + '_')


@pytest.fixture()
def fixed_datetime(monkeypatch):
	"""
	Pytest fixture to pretend the current datetime is 2:20 AM on 13th October 2020.

	.. seealso:: The :func:`~.with_fixed_datetime` contextmanager.

	.. attention::

		The monkeypatching only works when datetime is used and imported like:

		.. code-block:: python

			import datetime
			print(datetime.datetime.now())

		Using ``from datetime import datetime`` won't work.
	"""

	with with_fixed_datetime(datetime.datetime(2020, 10, 13, 2, 20)):
		yield


@pytest.fixture(
		params=[
				pytest.param(
						'/',
						id="forward",
						marks=pytest.mark.skipif(
								os.sep == '\\', reason=r"Output differs on platforms where os.sep == '\\'"
								)
						),
				pytest.param(
						'\\',
						id="backward",
						marks=pytest.mark.skipif(
								os.sep == '/', reason="Output differs on platforms where os.sep == '/'"
								)
						),
				]
		)
def path_separator(request) -> str:
	r"""
	Parametrized pytest fixture which returns the current filesystem path separator and skips the test for the other.

	This is useful when the test output differs on platforms with ``\`` as the path separator, such as windows.

	.. versionadded:: 0.4.0

	:rtype:

	.. clearpage::
	"""

	return request.param
