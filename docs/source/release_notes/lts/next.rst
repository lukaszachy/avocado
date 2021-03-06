.. _lts_next:

============
The Next LTS
============

The Long Term Stability releases of Avocado are the result of the
accumulated changes on regular (non-LTS) releases.

This section tracks the changes introduced on each regular (non-LTS)
Avocado release, and gives a sneak preview of what will make into the
next LTS release.

What's new?
===========

When compared to the last LTS (52.x), the main changes to be
introduced by the next LTS version are:

* A new loader implementation, that reuses (and resembles) the YAML
  input used for the varianter yaml_to_mux plugin.  It allows the
  definition of test suite based on a YAML file, including different
  variants for different tests.  For more information refer to
  :ref:`yaml_loader`.

* A better handling of interruption related signals, such as
  ``SIGINT`` and ``SIGTERM``.  Avocado will now try harder to not
  leave test processes that don't respond to those signals, and will
  itself behave better when it receives them.  For a complete
  description refer to :ref:`signal_handlers`.

* The output generated by tests on ``stdout`` and ``stderr`` are now
  properly prefixed with ``[stdout]`` and ``[stderr]`` in the
  ``job.log``.  The prefix is **not** applied in the case of
  ``$test_result/stdout`` and ``$test_result/stderr`` files, as one
  would expect.

* Test writers will get better protection against mistakes when trying
  to overwrite :class:`avocado.core.test.Test` "properties".  Some of
  those were previously implemented using
  :func:`avocado.utils.data_structures.LazyProperty` which did not
  prevent test writers from overwriting them.

* Avocado can now run list and run standard Python unittests, that is,
  tests written in Python that use the :mod:`unittest` library alone.

* Improvements in the serialization of TestIDs allow test result
  directories to be properly stored and accessed on Windows based
  filesystems.

* The complete output of tests, that is the combination of ``STDOUT``
  and ``STDERR`` is now also recorded in the test result directory as
  a file named ``output``.

* Support for listing and running golang tests has been introduced.
  Avocado can now discover tests written in Go, and if Go is properly
  installed, Avocado can run them.

* The support for test data files has been improved to support more
  specific sources of data.  For instance, when a test file used to
  contain more than one test, all of them shared the same ``datadir``
  property value, thus the same directory which contained data files.
  Now, tests should use the newly introduced :meth:`get_data()
  <avocado.core.test.TestData.get_data>` API, which will attempt to
  locate data files specific to the variant (if used), test name, and
  finally file name.  For more information, please refer to the
  section :ref:`accessing-test-data-files`.

* The output check feature will now use the to the most specific data
  source location available, which is a consequence of the switch to
  the use of the ``get_data()`` API discussed previously.  This means
  that two tests in a single file can generate different output,
  generate different ``stdout.expected`` or ``stderr.expected``.

* When the output check feature finds a mismatch between expected and
  actual output, will now produce a unified diff of those, instead of
  printing out their full content.  This makes it a lot easier to
  read the logs and quickly spot the differences and possibly the
  failure cause(s).

* Sysinfo collection can now be enabled on a test level basis.

* The locations of ``/etc`` (config) and ``/usr/libexec`` (libexec)
  files changed to live within the pkg_data (eg.
  ``/usr/lib/python2.7/site-packages/avocado/etc``) by default
  in order to not to modify files outside the package dir, which
  allowes shipping wheel packages and user installation. Distributions
  might still modify this to better follow their conventions (eg.
  for RPM the original locations are used)

* The exception raised by the utility functions in
  :mod:`avocado.utils.memory` has been renamed from ``MemoryError``
  and became :class:`avocado.utils.memory.MemError`.  The reason is
  that ``MemoryError`` is a Python standard exception, that is
  intended to be used on different situations.

Complete list of changes
========================

For a complete list of changes between the last LTS release (52.0) and
this release, please check out `the Avocado commit changelog
<https://github.com/avocado-framework/avocado/compare/52.0...master>`_.
