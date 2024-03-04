############
coincidence
############

.. start short_desc

**Helper functions for pytest.**

.. end short_desc


.. start shields

.. list-table::
	:stub-columns: 1
	:widths: 10 90

	* - Docs
	  - |docs| |docs_check|
	* - Tests
	  - |actions_linux| |actions_windows| |actions_macos| |coveralls|
	* - PyPI
	  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
	* - Anaconda
	  - |conda-version| |conda-platform|
	* - Activity
	  - |commits-latest| |commits-since| |maintained| |pypi-downloads|
	* - QA
	  - |codefactor| |actions_flake8| |actions_mypy|
	* - Other
	  - |license| |language| |requires|

.. |docs| image:: https://img.shields.io/readthedocs/coincidence/latest?logo=read-the-docs
	:target: https://coincidence.readthedocs.io/en/latest
	:alt: Documentation Build Status

.. |docs_check| image:: https://github.com/python-coincidence/coincidence/workflows/Docs%20Check/badge.svg
	:target: https://github.com/python-coincidence/coincidence/actions?query=workflow%3A%22Docs+Check%22
	:alt: Docs Check Status

.. |actions_linux| image:: https://github.com/python-coincidence/coincidence/workflows/Linux/badge.svg
	:target: https://github.com/python-coincidence/coincidence/actions?query=workflow%3A%22Linux%22
	:alt: Linux Test Status

.. |actions_windows| image:: https://github.com/python-coincidence/coincidence/workflows/Windows/badge.svg
	:target: https://github.com/python-coincidence/coincidence/actions?query=workflow%3A%22Windows%22
	:alt: Windows Test Status

.. |actions_macos| image:: https://github.com/python-coincidence/coincidence/workflows/macOS/badge.svg
	:target: https://github.com/python-coincidence/coincidence/actions?query=workflow%3A%22macOS%22
	:alt: macOS Test Status

.. |actions_flake8| image:: https://github.com/python-coincidence/coincidence/workflows/Flake8/badge.svg
	:target: https://github.com/python-coincidence/coincidence/actions?query=workflow%3A%22Flake8%22
	:alt: Flake8 Status

.. |actions_mypy| image:: https://github.com/python-coincidence/coincidence/workflows/mypy/badge.svg
	:target: https://github.com/python-coincidence/coincidence/actions?query=workflow%3A%22mypy%22
	:alt: mypy status

.. |requires| image:: https://dependency-dash.repo-helper.uk/github/python-coincidence/coincidence/badge.svg
	:target: https://dependency-dash.repo-helper.uk/github/python-coincidence/coincidence/
	:alt: Requirements Status

.. |coveralls| image:: https://img.shields.io/coveralls/github/python-coincidence/coincidence/master?logo=coveralls
	:target: https://coveralls.io/github/python-coincidence/coincidence?branch=master
	:alt: Coverage

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/python-coincidence/coincidence?logo=codefactor
	:target: https://www.codefactor.io/repository/github/python-coincidence/coincidence
	:alt: CodeFactor Grade

.. |pypi-version| image:: https://img.shields.io/pypi/v/coincidence
	:target: https://pypi.org/project/coincidence/
	:alt: PyPI - Package Version

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/coincidence?logo=python&logoColor=white
	:target: https://pypi.org/project/coincidence/
	:alt: PyPI - Supported Python Versions

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/coincidence
	:target: https://pypi.org/project/coincidence/
	:alt: PyPI - Supported Implementations

.. |wheel| image:: https://img.shields.io/pypi/wheel/coincidence
	:target: https://pypi.org/project/coincidence/
	:alt: PyPI - Wheel

.. |conda-version| image:: https://img.shields.io/conda/v/domdfcoding/coincidence?logo=anaconda
	:target: https://anaconda.org/domdfcoding/coincidence
	:alt: Conda - Package Version

.. |conda-platform| image:: https://img.shields.io/conda/pn/domdfcoding/coincidence?label=conda%7Cplatform
	:target: https://anaconda.org/domdfcoding/coincidence
	:alt: Conda - Platform

.. |license| image:: https://img.shields.io/github/license/python-coincidence/coincidence
	:target: https://github.com/python-coincidence/coincidence/blob/master/LICENSE
	:alt: License

.. |language| image:: https://img.shields.io/github/languages/top/python-coincidence/coincidence
	:alt: GitHub top language

.. |commits-since| image:: https://img.shields.io/github/commits-since/python-coincidence/coincidence/v0.6.6
	:target: https://github.com/python-coincidence/coincidence/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/python-coincidence/coincidence
	:target: https://github.com/python-coincidence/coincidence/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2024
	:alt: Maintenance

.. |pypi-downloads| image:: https://img.shields.io/pypi/dm/coincidence
	:target: https://pypi.org/project/coincidence/
	:alt: PyPI - Downloads

.. end shields

Installation
--------------

.. start installation

``coincidence`` can be installed from PyPI or Anaconda.

To install with ``pip``:

.. code-block:: bash

	$ python -m pip install coincidence

To install with ``conda``:

	* First add the required channels

	.. code-block:: bash

		$ conda config --add channels https://conda.anaconda.org/conda-forge
		$ conda config --add channels https://conda.anaconda.org/domdfcoding

	* Then install

	.. code-block:: bash

		$ conda install coincidence

.. end installation
