===============
Changelog
===============

0.6.0
----------

:func:`coincidence.PEP_563` is temporarily set to :py:obj:`False` for all versions until the future of typing PEPs has been determined.
No released versions of Python currently have :pep:`563` enabled by default.


0.5.0
----------

* :meth:`coincidence.regressions.AdvancedDataRegressionFixture` -- Add support for :mod:`pathlib`
  and :class:`domdf_python_tools.paths.PathPlus`.


0.4.3
-------------

Bugs Fixed
^^^^^^^^^^^^^

* :func:`coincidence.utils.with_fixed_datetime` -- Correctly handle monkeypatching of datetime in PyPy.

0.4.1
-------------

Bugs Fixed
^^^^^^^^^^^^^

* :func:`coincidence.PEP_563` -- Is now :py:obj:`True` on Python >=3.11, per the deferral of :pep:`563`.

0.4.0
----------

.. changelog:: 0.4.0


0.3.1
----------

Bugs Fixed
^^^^^^^^^^^^^

:mod:`coincidence.regressions` -- Ensure the custom YAML representers are only configured if PyYAML can be imported.


0.3.0
----------

:class:`coincidence.regressions.AdvancedDataRegressionFixture`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Handle ``toml.decoder.InlineTableDict`` the ``toml`` module is available.
* Improve handling of custom subclasses, especially for nested types.


0.2.3
----------

Bugs Fixed
^^^^^^^^^^^^^

Disabled the entry point as it was resulting in a confused plugin loading order and did not work.

The way of enabling the plugin reverts to:

.. code-block:: python

	# conftest.py
	pytest_plugins = ("coincidence", )


0.2.0
----------

* Switched to whey_ as the build backend.
* Added support for PyPy 3.7
* :del:`Added an entry point for pytest to avoid the need to enable the plugin in conftest.` (reverted in 0.2.3)

.. _whey: https://whey.readthedocs.io/en/latest/

.. changelog:: 0.2.0


0.1.2
----------

* :meth:`coincidence.regressions.AdvancedDataRegressionFixture.check` -- Add support for ``_pytest.capture.CaptureResult``.


0.1.1
----------

* :class:`coincidence.regressions.AdvancedDataRegressionFixture` -- Add a fake version when PyYAML cannot be imported.


0.1.0
----------

Initial release.
