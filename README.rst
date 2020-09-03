Flinx
=====

Configuration-free Sphinx package documentation.

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

.. warning:: TODO: Currently this pollutes ``./docs``.

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

If pyproject.toml_ exists and contains a ``[tool.flinx.metadata]`` table, the
project name, author, version, copyright date (``date``), and description file
are read from that. These are all optional.

If ``pyproject.toml`` contains a ``[tool.flit.metadata]`` Flit_
configuration table, the project name, author, and description file are read
from that.

If ``pyproject.toml`` contains a ``[tool.poetry]`` Poetry_ configuration table,
the project name, author, and version are read from that.

Flinx attempts to automatically discover any information that isn't specified in
the project file:

* Flinx attempts to detect the module. This is the first non-test
  directory that contains an ``__init__.py`` file that contains a version
  definition, else it's the first non-test ``*.py`` file that contains a version
  definition. A version definition is a line of the format ``__version__ =
  "1.2.3"``, with single or double quotes. (Flinx ignores whitespace, but does
  not import or parse the file.)
* Flix reads the version from the module file (if the module is a single file), or from the
  module's `__init__.py` file (if the module is a directory).
* The author is read from `git config user.name`. It's an error if there's
  no project file, and the author isn't available via git.
* The copyright date is the current year.

Add `Sphinx configuration`_ variables to a ``[tool.flinx.configuration]`` table
in ``pyproject.toml``. For example:

::

  [tool.flinx.configuration]
  html_theme = 'sphinx_rtd_theme'

Extensions in the ``sphinx.ext`` namespace can be abbreviated. For example,
``extensions = ['napoleon', 'todo']`` is equivalent to ``extensions =
['sphinx.ext.napoleon', 'sphinx.ext.todo']``.

Extensions from ``sphinx.ext`` are automatically added, if there's a
configuration variable that begins with the name of that estension. For example,
the presence of ``todo_include_todos = true`` in the project file implies
``sphinx.ext.todo``.

.. _pyproject.toml: https://www.python.org/dev/peps/pep-0518/
.. _Flit: https://flit.readthedocs.io/en/latest/
.. _Poetry: https://poetry.eustace.io
.. _Sphinx configuration: http://www.sphinx-doc.org/en/master/usage/configuration.html

Limitations
-----------

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
