from functools import reduce
from pathlib import Path

import pytoml as toml


def get_sphinx_configuration(project_dir):
    """Read the Sphinx configuration from ``pyproject.toml```."""
    try:
        project = toml.loads((Path(project_dir) / 'pyproject.toml').read_text())
        return reduce(lambda a, b: a[b], 'tool.flinx.configuration'.split('.'), project)
    except (FileNotFoundError, KeyError):
        return {}
