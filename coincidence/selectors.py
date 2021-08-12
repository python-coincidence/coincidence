#!/usr/bin/env python
#
#  selectors.py
"""
Pytest decorators for selectively running tests.
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
import inspect
import sys
from textwrap import dedent
from typing import Callable, Optional, Tuple, Union, cast

# 3rd party
import pytest
from _pytest.mark import MarkDecorator  # nodep
from domdf_python_tools.compat import PYPY
from domdf_python_tools.versions import Version

# this package
from coincidence.utils import is_docker

__all__ = [
		"min_version",
		"max_version",
		"only_version",
		"not_windows",
		"only_windows",
		"not_pypy",
		"only_pypy",
		"not_macos",
		"only_macos",
		"not_docker",
		"not_linux",
		"only_linux",
		"only_docker",
		"platform_boolean_factory",
		]


def _make_version(version: Union[str, float, Tuple[int, ...]]) -> Version:
	if isinstance(version, float):
		return Version.from_float(version)
	elif isinstance(version, str):
		return Version.from_str(version)
	else:
		return Version.from_tuple(version)


def min_version(
		version: Union[str, float, Tuple[int, ...]],
		reason: Optional[str] = None,
		) -> MarkDecorator:
	"""
	Factory function to return a ``@pytest.mark.skipif`` decorator which will
	skip a test if the current Python version is less than the required one.

	:param version: The version number to compare to :py:data:`sys.version_info`.
	:param reason: The reason to display when skipping.
	:default reason: :file:`'Requires Python {<version>} or greater.'`
	"""  # noqa: D400

	version_ = _make_version(version)

	if reason is None:  # pragma: no cover
		reason = f"Requires Python {version_} or greater."

	return pytest.mark.skipif(condition=sys.version_info[:3] < version_, reason=reason)


def max_version(
		version: Union[str, float, Tuple[int, ...]],
		reason: Optional[str] = None,
		) -> MarkDecorator:
	"""
	Factory function to return a ``@pytest.mark.skipif`` decorator which will
	skip a test if the current Python version is greater than the required one.

	:param version: The version number to compare to :py:data:`sys.version_info`.
	:param reason: The reason to display when skipping.
	:default reason: :file:`'Not needed after Python {<version>}.'`
	"""  # noqa: D400

	version_ = _make_version(version)

	if reason is None:  # pragma: no cover
		reason = f"Not needed after Python {version_}."

	return pytest.mark.skipif(condition=sys.version_info[:3] > version_, reason=reason)


def only_version(
		version: Union[str, float, Tuple[int, ...]],
		reason: Optional[str] = None,
		) -> MarkDecorator:
	"""
	Factory function to return a ``@pytest.mark.skipif`` decorator which will
	skip a test if the current Python version not the required one.

	:param version: The version number to compare to :py:data:`sys.version_info`.
	:param reason: The reason to display when skipping.
	:default reason: :file:`'Not needed on Python {<version>}.'`
	"""  # noqa: D400

	version_ = _make_version(version)

	if reason is None:  # pragma: no cover
		reason = f"Not needed on Python {version_}."

	return pytest.mark.skipif(condition=sys.version_info[:2] != version_[:2], reason=reason)


def platform_boolean_factory(
		condition: bool,
		platform: str,
		versionadded: Optional[str] = None,
		*,
		module: Optional[str] = None,
		) -> Tuple[Callable[..., MarkDecorator], Callable[..., MarkDecorator]]:
	"""
	Factory function to return decorators such as :func:`~.not_pypy` and :func:`~.only_windows`.

	:param condition: Should evaluate to :py:obj:`True` if the test should be skipped.
	:param platform:
	:param versionadded:
	:param module: The module to set the function as belonging to in ``__module__``.
		If :py:obj:`None` ``__module__`` is set to ``'coincidence.selectors'``.

	:return: 2-element tuple of ``not_function``, ``only_function``.
	"""

	default_reason = f"{{}} required on {platform}"
	module = module or platform_boolean_factory.__module__

	def not_function(reason: str = default_reason.format("Not")) -> MarkDecorator:
		return pytest.mark.skipif(condition=condition, reason=reason)

	def only_function(reason: str = default_reason.format("Only")) -> MarkDecorator:
		return pytest.mark.skipif(condition=not condition, reason=reason)

	docstring = dedent(
			"""\
Factory function to return a ``@pytest.mark.skipif`` decorator which will
skip a test {why} the current platform is {platform}.

{versionadded_string}
:param reason: The reason to display when skipping.
"""
			)

	if versionadded:
		versionadded_string = f".. versionadded:: {versionadded}\n"
	else:
		versionadded_string = ''

	not_function.__name__ = not_function.__qualname__ = f"not_{platform.lower()}"
	not_function.__module__ = module
	not_function.__doc__ = docstring.format(why="if", platform=platform, versionadded_string=versionadded_string)

	only_function.__name__ = only_function.__qualname__ = f"only_{platform.lower()}"
	only_function.__module__ = module
	only_function.__doc__ = docstring.format(
			why="unless", platform=platform, versionadded_string=versionadded_string
			)

	return not_function, only_function


not_windows, only_windows = platform_boolean_factory(condition=sys.platform == "win32", platform="Windows")
only_windows.__doc__ = f"""\
{inspect.cleandoc(only_windows.__doc__ or '')}

:rtype:

.. latex:clearpage::
"""

not_macos, only_macos = platform_boolean_factory(condition=sys.platform == "darwin", platform="macOS")

not_linux, only_linux = platform_boolean_factory(
		condition=sys.platform == "linux",
		platform="Linux",
		versionadded="0.2.0"
		)
not_linux.__doc__ = f"""\
{inspect.cleandoc(not_linux.__doc__ or '')}

:rtype:

.. latex:clearpage::
"""

not_docker, only_docker = platform_boolean_factory(condition=is_docker(), platform="Docker")
not_docker.__doc__ = cast(str, not_docker.__doc__).replace("the current platform is", "running on")
only_docker.__doc__ = cast(str, only_docker.__doc__).replace("the current platform is", "running on")

not_pypy, only_pypy = platform_boolean_factory(condition=PYPY, platform="PyPy")
not_pypy.__doc__ = cast(str, not_pypy.__doc__).replace("current platform", "current Python implementation")
only_pypy.__doc__ = cast(str, only_pypy.__doc__).replace("current platform", "current Python implementation")
