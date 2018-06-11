Flinx
=====

Configuration Python package documentation, using Sphinx.

Flinx aims to be for documentation as Flit is for packaging.

Installation
------------

::

    $ python3 -m pip install flinx

Usage
-----

``flinx`` or ``flinx build`` builds the documentation.

With no ``pyproject.toml``: documents all the non-test \*.py files, and directories that contain an ``__init__.py``.

``flinx serve`` runs via autosphinx. With `-o` or `--open`, opens the documentation in a browser.

``flinx build`` generates a ``docs/conf.py`` file, for compatability with etc.
``flinx build --force`` overwrites an existing file.

Benefits
--------

Doesn't require any files. Autodiscover and markdown by default. Update the
project name and version.

Configuration
-------------

Acknowledements
---------------

Inspired by flit. Built on sphinx and autosphinx.

License
-------

MIT
