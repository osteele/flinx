Flinx
=====

.. warning::
   Work in progress. Don't use me yet!

Configuration-free Sphinx package documentation.

Flinx aims to be for documentation as Flit is for packaging.

Signs you might be interested in this package:

* You want zero-configuration documentation for new projects.
* You're tired of manually editing both your module source, and ```conf.py``, when
  you rename your module. (I know, you shouldn't do this after you've published.
  But I do this a lot during initial development.)
* You're tired of manually editing both your module source, and ``conf.py``,
  when you bump the version number. (Although `bumpversion
  <https://github.com/peritus/bumpversion>`_ is an alternative, here.)
* You're an eager guinea pig for early-stage software.

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

``flinx generate`` writes ``docs/conf.py`` and ``docs/index.rst``, that match
the current project settings. TODO: It will balk if these files already exist.

``flinx eject`` is equivalent to ``flinx generate``, except that the files omit
the "THIS FILE IS GENERATED AUTOMATICALLY BY FLINX. MANUAL CHANGES WILL BE LOST"
warning in the header.

TODO: ``flinx generate --force`` overwrites existing files.

TODO: ``flinx install`` installs required extensions. If a `Pipfile` exists,
it uses `pipenv install --dev` to install them. ``flinx install -r`` adds them
to ``requirements.txt``. ``flinx install -rdev-requirements.txt`` adds them to
``dev-requirements.txt``.

.. note::
   These command-line options are pretty different from ``sphinx-build`` and
   ``sphinx-autobuild``. This falls under the heading of “if you're happy with
   those tools and know your way around their options, you probably won't like
   this package”. They're designed to be more like *other* site generators that
   I use, such as Jekyll. Since I *don't* know my way around ``sphinx-build``,
   I'm not trying to be compatible with it.

Configuration
-------------

When a `pyproject.toml <https://www.python.org/dev/peps/pep-0518/>`_ file is
present, the module name, author, and description file are read from its
``[tool.flit.metadata]`` section.

TODO: Otherwise: this documents all the non-test \*.py files, and directories
that contain an ``__init__.py``.

TODO: Configure Sphinx options,by adding sections to ``pyproject.toml``. (Maybe
they should go in ``setup.cfg`` instead.)

Limitations
-----------

Doesn't allow customization. (WIP.)

Isn't compatible with Read the Docs. (Planned, but tricky.)

Acknowledements
---------------

Inspired by `flit <https://flit.readthedocs.io/en/latest/>`_. Built on `sphinx
<http://www.sphinx-doc.org/en/master/>`_ and `sphinx-autobuild
<https://github.com/GaretJax/sphinx-autobuild>`_.

About the Name
--------------

“Flinx” is a mash-up of “flit” and “sphinx”. I wanted to name it “flynx”, as a
tribute to `Seveneves <https://en.wikipedia.org/wiki/Seveneves>`_, but I
realized I'd been spelling “sphinx” wrong. There's an app named “Flynx”, so it's
probably just as well.

“Flinx” is also a character in an Allen Dean Foster series. I regret to admit
that I haven't read that series, and that it didn't inform my choice of names.

License
-------

MIT
