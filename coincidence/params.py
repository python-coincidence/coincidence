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

# stdlib
import itertools
import random
from typing import Sequence

# 3rd party
import pytest
from _pytest.mark import MarkDecorator  # nodep

# this package
from coincidence.utils import generate_falsy_values, generate_truthy_values, whitespace_perms_list

__all__ = ["count", "testing_boolean_values", "whitespace_perms"]

MarkDecorator.__module__ = "_pytest.mark"


def testing_boolean_values(
		extra_truthy: Sequence = (),
		extra_falsy: Sequence = (),
		ratio: float = 1,
		) -> MarkDecorator:
	"""
	Returns a `pytest.mark.parametrize <https://docs.pytest.org/en/stable/parametrize.html>`_
	decorator that provides a list of strings, integers and booleans, and the boolean representations of them.

	The parametrized arguments are ``boolean_string`` for the input value,
	and ``expected_boolean`` for the expected output.

	Optionally, a random selection of the values can be returned using the ``ratio`` argument.

	:param extra_truthy: Additional values that should be considered :py:obj:`True`.
	:param extra_falsy: Additional values that should be considered :py:obj:`False`.
	:param ratio: The ratio of the number of values to select to the total number of values.
	"""  # noqa D400

	truthy = generate_truthy_values(extra_truthy, ratio)
	falsy = generate_falsy_values(extra_falsy, ratio)

	boolean_strings = [
			*itertools.zip_longest(truthy, [], fillvalue=True),
			*itertools.zip_longest(falsy, [], fillvalue=False),
			]

	return pytest.mark.parametrize("boolean_string, expected_boolean", boolean_strings)


def whitespace_perms(ratio: float = 0.5) -> MarkDecorator:
	r"""
	Returns a `pytest.mark.parametrize <https://docs.pytest.org/en/stable/parametrize.html>`_
	decorator that provides permutations of whitespace (strictly only ``␣\n\t\r``).
	Not all permutations are returned, as there are a lot of them;
	instead a random selection of the permutations is returned.
	By default ½ of the permutations are returned, but this can be configured using the ``ratio`` argument.

	The single parametrized argument is ``char``.

	:param ratio: The ratio of the number of permutations to select to the total number of permutations.
	"""  # noqa D400

	perms = whitespace_perms_list()
	return pytest.mark.parametrize("char", random.sample(perms, int(len(perms) * ratio)))


def count(stop: int, start: int = 0, step: int = 1) -> MarkDecorator:
	"""
	Returns a `pytest.mark.parametrize <https://docs.pytest.org/en/stable/parametrize.html>`_
	decorator that provides a list of numbers between ``start`` and ``stop`` with an interval of ``step``.

	The single parametrized argument is ``count``.

	:param stop: The stop value passed to :class:`range`.
	:param start: The start value passed to :class:`range`.
	:param step: The step passed to :class:`range`.
	"""  # noqa D400

	return pytest.mark.parametrize("count", range(start, stop, step))
