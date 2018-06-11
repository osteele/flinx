Flinx
=====

.. warning::
  Work in progress. Don't use yet!

Configuration-free Sphinx package documentation.

Flinx aims to be for documentation as Flit is for packaging.

Signs you might be interested in this package:

* You want zero-configuration documentation for new projects.
* You're tired of manually editing both your module source, and `conf.py`, when
  you change your mind about your module name. (I know, this shouldn't happen
  much. But I do this a lot during initial development.)
* You're tired of manually editing both your module source, and `conf.py`, when
  you bump the version number. (Although `bumpversion
  <https://github.com/peritus/bumpversion>`_ is an alternative, here.)
* You're okay trying early-stage software.

Signs you won't be interested in (and will probably dislike) this package:

* You're happy using ``sphinx-quickstart`` to create ``docs/conf.py`` and
  ``docs/Makefile``
* You know your way around Sphinx ``conf.py``, ``sphinx-build``, and
  ``sphinx--autobuild``.
* In general, the standard Sphinx tooling works just fine for you.
* You don't want to try early-stage software.

Installation
------------

::

    $ python3 -m pip install flinx

Usage
-----

``flinx`` or ``flinx build`` builds the HTML documentation.

``flinx --open`` opens a browser onto the documentation once it's built.

TODO: ``flinx watch`` runs via autosphinx. With ``-o`` or ``--open``, opens the
documentation in a browser.

TODO: ``flinx generate`` writes ``docs/conf.py`` and ``docs/index.rst``, that match the
current project settings. It will balk if these files already exist.

Use this to "eject" flinx.

TODO: ``flinx generate --force`` overwrites existing files.

TODO: ``flinx install`` installs required extensions. If a `Pipfile` exists,
it uses `pipenv install --dev` to install them. ``flinx install -r`` adds them
to ``requirements.txt``. ``flinx install -rdev-requirements.txt`` adds them to
``dev-requirements.txt``.

Benefits
--------

Doesn't require any configuration files. Always uses the current package name
and version. TODO: Autodiscover and markdown by default.

Configuration
-------------

With no ``pyproject.toml``: documents all the non-test \*.py files, and directories that contain an ``__init__.py``.

TBD. Basically, this will be adding sections to ``pyproject.toml``, but maybe
they should go in ``setup.cfg`` instead.

Limitations
-----------

Doesn't allow customization. (WIP.)

Isn't compatible with Read the Docs. (Planned, but tricky.)

Acknowledements
---------------

Inspired by `flit <https://flit.readthedocs.io/en/latest/>`. Built on `sphinx
<http://www.sphinx-doc.org/en/master/>`_ and `sphinx-autobuild
<https://github.com/GaretJax/sphinx-autobuild>`_.

License
-------

MIT
