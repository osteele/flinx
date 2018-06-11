"""Configuration-free Python doc generation via Sphinx."""

import sys
import webbrowser
from pathlib import Path

from jinja2 import Environment, PackageLoader, select_autoescape

import pytoml as toml
from sphinx.cmd.build import main as sphinx

__version__ = '0.1.0'

env = Environment()
env.filters['repr'] = repr
poject_relpath = Path('..')
env.filters['project_rel'] = lambda s: str(poject_relpath / s)

TEMPLATE_DIR = Path('templates')
conf_tpl = env.from_string((TEMPLATE_DIR / 'conf.py.tpl').read_text())
index_tpl = env.from_string((TEMPLATE_DIR / 'index.rst.tpl').read_text())


def build(output_dir):
    """Generate the ``conf.py`` and ``README.rst`` files."""
    index_text = index_tpl.render(
        readme_path='README.rst',
        module_name='flinx',
    )
    (output_dir / 'index.rst').write_text(index_text)
    conf_text = conf_tpl.render(
        module_path='..',
        project='flinx',
        copyright='2018, Oliver Steele',
        author='Oliver Steele',
        version='0.1.0',
        language='en',
        extensions=['sphinx.ext.intersphinx'],
        master_basename='index',
    )
    conf_path = output_dir / 'conf.py'
    conf_path.write_text(conf_text)
    return conf_path


def main():
    """Build the documentation."""
    docs_dir = Path('./docs')
    build_dir = docs_dir / '_build'
    docs_dir.mkdir(exist_ok=True)
    conf_path = build(docs_dir)
    status = sphinx([
        '-a',  # always build
        '-c', str(conf_path.parent),  # config file
        '-j', 'auto',  # processors
        '-q',  # quiet
        str(docs_dir),
        str(build_dir)
    ])
    if status:
        sys.exit(sys.exit)
    webbrowser.open(str(build_dir / 'index.html'))


if __name__ == '__main__':
    main()
