#!/usr/bin/env python
#
#  params.py
"""
`pytest.mark.parametrize <https://docs.pytest.org/en/stable/parametrize.html>`_ decorators.
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
#  "param" based on pytest
#  Copyright (c) 2004-2020 Holger Krekel and others
#  MIT Licensed
#

# stdlib
import itertools
import random
from typing import Callable, Collection, Iterable, List, Optional, Sequence, Tuple, TypeVar, Union, cast, overload

# 3rd party
import pytest
from _pytest.mark import Mark, MarkDecorator, ParameterSet  # nodep
from domdf_python_tools.iterative import extend_with_none

# this package
from coincidence.selectors import _make_version, only_version
from coincidence.utils import generate_falsy_values, generate_truthy_values, whitespace_perms_list

__all__ = ["count", "whitespace_perms", "testing_boolean_values", "param", "parametrized_versions"]

_T = TypeVar("_T")
MarkDecorator.__module__ = "_pytest.mark"


def testing_boolean_values(
		extra_truthy: Sequence = (),
		extra_falsy: Sequence = (),
		ratio: float = 1,
		) -> MarkDecorator:
	"""
	Returns a `pytest.mark.parametrize <https://docs.pytest.org/en/stable/parametrize.html>`__
	decorator which provides a list of strings, integers and booleans, and the boolean representations of them.

	The parametrized arguments are ``boolean_string`` for the input value,
	and ``expected_boolean`` for the expected output.

	Optionally, a random selection of the values can be returned using the ``ratio`` argument.

	:param extra_truthy: Additional values to treat as :py:obj:`True`.
	:param extra_falsy: Additional values to treat as :py:obj:`False`.
	:param ratio: The ratio of the number of values to select to the total number of values.
	"""  # noqa: D400

	truthy = generate_truthy_values(extra_truthy, ratio)
	falsy = generate_falsy_values(extra_falsy, ratio)

	boolean_strings = [
			*itertools.zip_longest(truthy, [], fillvalue=True),
			*itertools.zip_longest(falsy, [], fillvalue=False),
			]

	return pytest.mark.parametrize("boolean_string, expected_boolean", boolean_strings)


def whitespace_perms(ratio: float = 0.5) -> MarkDecorator:
	r"""
	Returns a `pytest.mark.parametrize <https://docs.pytest.org/en/stable/parametrize.html>`__
	decorator which provides permutations of whitespace.

	For this function whitespace is only ``␣\n\t\r``.

	Not all permutations are returned, as there are a lot of them;
	instead a random selection of the permutations is returned.
	By default ½ of the permutations are returned, but this can be configured using the ``ratio`` argument.

	The single parametrized argument is ``char``.

	:param ratio: The ratio of the number of permutations to select to the total number of permutations.
	"""  # noqa: D400

	perms = whitespace_perms_list()
	return pytest.mark.parametrize("char", random.sample(perms, int(len(perms) * ratio)))


def count(stop: int, start: int = 0, step: int = 1) -> MarkDecorator:
	"""
	Returns a `pytest.mark.parametrize <https://docs.pytest.org/en/stable/parametrize.html>`__
	decorator which provides a list of numbers between ``start`` and ``stop`` with an interval of ``step``.

	The single parametrized argument is ``count``.

	:param stop: The stop value passed to :class:`range`.
	:param start: The start value passed to :class:`range`.
	:param step: The step passed to :class:`range`.
	"""  # noqa: D400

	return pytest.mark.parametrize("count", range(start, stop, step))


@overload
def param(
		*values: object,
		marks: Union[MarkDecorator, Collection[Union[MarkDecorator, Mark]]] = (),
		id: Optional[str] = ...,  # noqa: A002  # pylint: disable=redefined-builtin
		) -> ParameterSet: ...


@overload
def param(
		*values: object,
		marks: Union[MarkDecorator, Collection[Union[MarkDecorator, Mark]]] = (),
		idx: Optional[int],
		) -> ParameterSet: ...


@overload
def param(
		*values: _T,
		marks: Union[MarkDecorator, Collection[Union[MarkDecorator, Mark]]] = (),
		key: Optional[Callable[[Tuple[_T, ...]], str]],
		) -> ParameterSet: ...


def param(
		*values: _T,
		marks: Union[MarkDecorator, Collection[Union[MarkDecorator, Mark]]] = (),
		id: Optional[str] = None,  # noqa: A002  # pylint: disable=redefined-builtin
		idx: Optional[int] = None,
		key: Optional[Callable[[Tuple[_T, ...]], str]] = None,
		) -> ParameterSet:
	r"""
	Specify a parameter in `pytest.mark.parametrize <https://docs.pytest.org/en/stable/parametrize.html>`__
	calls or :ref:`parametrized fixtures <fixture-parametrize-marks>`.

	**Examples:**

	.. code-block:: python

		@pytest.mark.parametrize("test_input, expected", [
			("3+5", 8),
			param("6*9", 42, marks=pytest.mark.xfail),
			param("2**2", 4, idx=0),
			param("3**2", 9, id="3^2"),
			param("sqrt(9)", 3, key=itemgetter(0)),
		])
		def test_eval(test_input, expected):
			assert eval (test_input) == expected

	.. versionadded:: 0.4.0

	:param \*values: Variable args of the values of the parameter set, in order.
	:param marks: A single mark or a list of marks to be applied to this parameter set.
	:param id: The id to attribute to this parameter set.
	:param idx: The index of the value in ``*values`` to use as the id.
	:param key: A callable which is given ``values`` (as a :class:`tuple`) and returns the value to use as the id.

	:rtype:

	.. clearpage::
	"""  # noqa: D400

	if len([x for x in (id, idx, key) if x is not None]) > 1:
		raise ValueError("'id', 'idx' and 'key' are mutually exclusive.")

	if idx is not None:
		# pytest will catch the type error later on
		id = cast(str, values[idx])  # noqa: A001  # pylint: disable=redefined-builtin
	elif key is not None:
		id = key(values)  # noqa: A001  # pylint: disable=redefined-builtin

	return ParameterSet.param(*values, marks=marks, id=id)


def parametrized_versions(
		*versions: Union[str, float, Tuple[int, ...]],
		reasons: Union[str, Iterable[Optional[str]]] = (),
		) -> List[ParameterSet]:
	r"""
	Return a list of parametrized version numbers.

	**Examples:**

	.. code-block:: python

		@pytest.mark.parametrize(
			"version",
			parametrized_versions(
				3.6,
				3.7,
				3.8,
				reason="Output differs on each version.",
				),
			)
		def test_something(version: str):
			pass


	.. code-block:: python

		@pytest.fixture(
			params=parametrized_versions(
				3.6,
				3.7,
				3.8,
				reason="Output differs on each version.",
				),
			)
		def version(request):
			return request.param

		def test_something(version: str):
			pass

	.. versionadded:: 0.4.0

	:param \*versions: The Python versions to parametrize.
	:param reasons: The reasons to use when skipping versions.
		Either a string value to use for all versions,
		or a list of values which correspond to ``*versions``.
	"""

	version_list = list(versions)
	params = []

	if isinstance(reasons, str):
		reasons = [reasons] * len(version_list)
	else:
		reasons = extend_with_none(reasons, len(version_list))

	for version, reason in zip(version_list, reasons):
		version_ = _make_version(version)

		the_param = pytest.param(
				f"{version_.major}.{version_.minor}",
				marks=only_version(version_, reason=reason),
				)

		params.append(the_param)

	return params
