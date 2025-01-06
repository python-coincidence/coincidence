#!/usr/bin/env python
#
#  utils.py
"""
Test helper utilities.
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
#  is_docker based on https://github.com/jaraco/jaraco.docker
#  Copyright Jason R. Coombs
#  MIT Licensed
#

# stdlib
import datetime
import os
import random
from contextlib import contextmanager
from functools import lru_cache
from itertools import chain, permutations
from typing import Any, Iterable, Iterator, List, Optional, Sequence, TypeVar, Union

# 3rd party
import pytest
from domdf_python_tools.compat import PYPY
from domdf_python_tools.iterative import Len
from domdf_python_tools.paths import PathPlus

__all__ = (
		"generate_truthy_values",
		"generate_falsy_values",
		"is_docker",
		"with_fixed_datetime",
		"whitespace",
		"whitespace_perms_list",
		)

_T = TypeVar("_T")

_cgroup = PathPlus("/proc/self/cgroup")
_dockerenv = "/.dockerenv"


def is_docker() -> bool:
	"""
	Returns whether the current Python instance is running in Docker.
	"""

	if os.path.exists(_dockerenv):
		return True

	if _cgroup.is_file():
		try:
			return any("docker" in line for line in _cgroup.read_lines())
		except FileNotFoundError:
			return False

	return False


class _DateMeta(type):  # pragma: no cover (PyPy)
	_date = datetime.date

	def __instancecheck__(self, instance: Any):  # noqa: MAN002
		return isinstance(instance, self._date)


class _DatetimeMeta(type):  # pragma: no cover (PyPy)
	_datetime = datetime.datetime

	def __instancecheck__(self, instance: Any) -> bool:
		return isinstance(instance, self._datetime)


@contextmanager
def with_fixed_datetime(fixed_datetime: datetime.datetime) -> Iterator:
	"""
	Context manager to set a fixed datetime for the duration of the ``with`` block.

	:param fixed_datetime:

	.. seealso:: The :fixture:`~.fixed_datetime` fixture.

	.. attention::

		The monkeypatching only works when datetime is used and imported like:

		.. code-block:: python

			import datetime
			print(datetime.datetime.now())

		Using ``from datetime import datetime`` won't work.
	"""

	if PYPY:  # pragma: no cover (!PyPy)

		with pytest.MonkeyPatch.context() as monkeypatch:
			monkeypatch.setattr(
					datetime.date,
					"today", lambda *args: datetime.date(
							fixed_datetime.year,
							fixed_datetime.month,
							fixed_datetime.day, )
					)
			monkeypatch.setattr(
					datetime.datetime,
					"today", lambda *args: datetime.datetime(
							fixed_datetime.year,
							fixed_datetime.month,
							fixed_datetime.day, )
					)
			monkeypatch.setattr(datetime.datetime, "now", lambda *args: fixed_datetime)

			yield

	else:  # pragma: no cover (PyPy)

		class D(datetime.date, metaclass=_DateMeta):

			@classmethod
			def today(cls) -> datetime.date:  # type: ignore[override]
				return datetime.date(
						fixed_datetime.year,
						fixed_datetime.month,
						fixed_datetime.day,
						)

		class DT(datetime.datetime, metaclass=_DatetimeMeta):

			@classmethod
			def today(cls) -> datetime.datetime:  # type: ignore[override]
				return datetime.datetime(
						fixed_datetime.year,
						fixed_datetime.month,
						fixed_datetime.day,
						)

			@classmethod
			def now(cls, tz: Optional[datetime.tzinfo] = None) -> datetime.datetime:  # type: ignore[override]
				return datetime.datetime.fromtimestamp(fixed_datetime.timestamp())

		D.__name__ = "date"
		D.__qualname__ = "date"
		DT.__qualname__ = "datetime"
		DT.__name__ = "datetime"
		D.__module__ = "datetime"
		DT.__module__ = "datetime"

		with pytest.MonkeyPatch.context() as monkeypatch:
			monkeypatch.setattr(datetime, "date", D)
			monkeypatch.setattr(datetime, "datetime", DT)

			yield


def generate_truthy_values(
		extra_truthy: Iterable[Union[str, int, _T]] = (),
		ratio: float = 1,
		) -> Iterator[Union[str, int, _T]]:
	"""
	Returns an iterator of strings, integers and booleans which should be considered :py:obj:`True`.

	Optionally, a random selection of the values can be returned using the ``ratio`` argument.

	:param extra_truthy: Additional values which should be considered :py:obj:`True`.
	:param ratio: The ratio of the number of values to select to the total number of values.
	"""

	truthy_values: Sequence[Union[str, int, _T]] = [
			True,
			"True",
			"true",
			"tRUe",
			'y',
			'Y',
			"YES",
			"yes",
			"Yes",
			"yEs",
			"ON",
			"on",
			'1',
			1,
			*extra_truthy,
			]

	if ratio < 1:
		truthy_values = random.sample(truthy_values, int(len(truthy_values) * ratio))

	yield from truthy_values


def generate_falsy_values(
		extra_falsy: Iterable[Union[str, int, _T]] = (),
		ratio: float = 1,
		) -> Iterator[Union[str, int, _T]]:
	"""
	Returns an iterator of strings, integers and booleans which should be considered :py:obj:`False`.

	Optionally, a random selection of the values can be returned using the ``ratio`` argument.

	:param extra_falsy: Additional values which should be considered :py:obj:`True`.
	:param ratio: The ratio of the number of values to select to the total number of values.
	"""

	falsy_values: Sequence[Union[str, int, _T]] = [
			False,
			"False",
			"false",
			"falSE",
			'n',
			'N',
			"NO",
			"no",
			"nO",
			"OFF",
			"off",
			"oFF",
			'0',
			0,
			*extra_falsy,
			]

	if ratio < 1:
		falsy_values = random.sample(falsy_values, int(len(falsy_values) * ratio))

	yield from falsy_values


whitespace = " \t\n\r"


@lru_cache(1)
def whitespace_perms_list() -> List[str]:  # noqa: D103
	perms = chain.from_iterable(permutations(whitespace, n) for n in Len(whitespace))
	return list(''.join(x) for x in perms)
