Flinx
=====

Configuration-free Sphinx package documentation.

.. warning::
   Work in progress. Beware!

Flinx aims to be for documentation what Flit is for packaging: a
configuration-free way to get started on {documentation, packaging}, and add
configuration gradually. It also borrows a concept from react-starter-kit: you
can “eject”, and leave Flinx behind.

This tool isn't for everyone. Flinx is a thin wrapper around ``sphinx-build``
and ``sphinx-autobuild``. If you're happy creating a ``docs/conf.py`` and using
those commands directly, you don't need this one.

Signs you might be interested in this package:

* You want zero-configuration documentation for new projects.
* You don't want to edit both your module source and ``conf.py``, when
  you rename your module. (I know, you shouldn't do this after you've published.
  But I do this a lot during initial development.)
* You don't want to manually edit both your module source, and ``conf.py``,
  when you bump the version number. (Although `bumpversion
  <https://github.com/peritus/bumpversion>`_ is an alternative, here.)
* You're an eager guinea pig for early-stage software.

Installation
------------

::

    $ python3 -m pip install flinx

Usage
-----

::

  $ flinx build

Uses `sphinx-build` to build the HTML documentation.

``flinx build -o`` opens a browser onto the documentation once it's been built.

.. todo:: Currently this pollutes ``./docs``.

::

  $ flinx serve

Uses ``sphinx-autobuild`` to build and serve the HTML documentation.

``flinx serve -o`` opens a browser onto the documentation once it's been built.

Thanks to ``sphinx-autobuild``, the documentation will re-build and re-run when
the sources are changed.

This doesn't extend to the ``pyproject.toml`` configuration file.

::

  $ flinx generate

Writes ``docs/conf.py`` and ``docs/index.rst``, that match the current project
settings.

::

  $ flinx eject

This is equivalent to ``flinx generate``, except that the files omit the "THIS
FILE IS AUTOMATICALLY GENERATED" warning in the header.

.. note::
   These command-line options are pretty different from ``sphinx-build`` and
   ``sphinx-autobuild``. This falls under the heading of “if you're happy with
   those tools and know your way around their options, you probably won't like
   this package”. They're designed to be more like *other* site generators that
   I use, such as Jekyll. Since I *don't* know my way around ``sphinx-build``,
   I'm not trying to be compatible with it.

Configuration
-------------

If pyproject.toml_ exists and has a Flit_ section ``[tool.flit.metadata]``, the
project name, author, and description file are read from that.

If ``pyproject.toml`` has a Poetry_ section ``[tool.poetry]``, the project name,
author, and version are read from that.

Otherwise, it attempts to detect the module. This is the first non-test
directory that contains an ``__init__.py`` file that contains a version
definition, else it's the first non-test \*.py file that contains a version
definition. A version definition is a line of the format ``__version__ =
"1.2.3"``, with single or double quotes.

Configure `Sphinx options`_ by adding sections to ``pyproject.toml``. For example:

::

  [tool.flinx]
  html_theme = 'sphinx_rtd_theme'

.. todo::

   Maybe these should go in ``setup.cfg`` instead.

.. _pyproject.toml: https://www.python.org/dev/peps/pep-0518/
.. _Flit: https://flit.readthedocs.io/en/latest/
.. _Poetry: https://poetry.eustace.io
.. _Sphinx options: http://www.sphinx-doc.org/en/master/usage/configuration.html

Limitations
-----------

Flinx doesn't currently allow Spinx customization. This is coming next.

Flinx isn't compatible with Read the Docs. This is planned, but tricky.

Acknowledgements
-----------------

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
