"""Configuration-free Python doc generation via Sphinx."""

import sys
import webbrowser
from pathlib import Path

import click
from jinja2 import Environment, PackageLoader, select_autoescape

from project_metadata import MetadataConfig
from sphinx.cmd.build import main as sphinx

__version__ = '0.1.0'

GENERATED_TEXT = "THIS FILE IS GENERATED AUTOMATICALLY BY FLINX. MANUAL CHANGES WILL BE LOST."

env = Environment()
env.filters['repr'] = repr
poject_relpath = Path('..')
env.filters['project_rel'] = lambda s: str(poject_relpath / s)

TEMPLATE_DIR = Path('templates')
conf_tpl = env.from_string((TEMPLATE_DIR / 'conf.py.tpl').read_text())
index_tpl = env.from_string((TEMPLATE_DIR / 'index.rst.tpl').read_text())


def write_template_files(output_dir, generated=True):
    """Generate the ``conf.py`` and ``README.rst`` files."""
    # TODO: refuse to overwrite non-generated ones
    metadata = MetadataConfig()
    generated_text = GENERATED_TEXT if generated else None
    index_text = index_tpl.render(
        readme=metadata['readme'],
        module_name=metadata['module'],
        generated_text=generated_text,
    )
    (output_dir / 'index.rst').write_text(index_text)
    copyright_year = '2018'
    author = metadata['author']
    conf_text = conf_tpl.render(
        module_path='..',
        project=metadata['module'],
        copyright=f'{copyright_year}, {author}',
        author=author,
        version=metadata['version'],
        language='en',
        # TODO: options for autodoc
        extensions=['sphinx.ext.autodoc', 'sphinx.ext.intersphinx'],
        source_suffix=['.rst'],
        master_basename='index',
        generated_text=generated_text,
    )
    conf_path = output_dir / 'conf.py'
    conf_path.write_text(conf_text)
    return conf_path


@click.group()
def main():
    pass


@main.command()
def generate():
    docs_dir = Path('./docs')
    write_template_files(docs_dir)


@main.command()
def eject():
    docs_dir = Path('./docs')
    write_template_files(docs_dir, generated=False)


@main.command()
@click.option('-a', '--all', is_flag=True,
              help='Rebuild all the docs, regardless of what has changed.')
@click.option('-o', '--open', is_flag=True,
              help='Open the HTML index in a browser.')
@click.option('--format', default='html',
              type=click.Choice(['html']),
              help='The output format.')
def build(all=False, format='html', open=False):
    """Build the documentation."""
    docs_dir = Path('./docs')
    build_dir = docs_dir / '_build' / format
    docs_dir.mkdir(exist_ok=True)
    conf_path = write_template_files(docs_dir)
    args = [
        '-b', format,
        '-c', str(conf_path.parent),  # config file
        '-j', 'auto',  # processors
        '-q',  # quiet
        str(docs_dir),
        str(build_dir)
    ]
    if all:
        args += ['-a']
    status = sphinx(args)
    if status:
        sys.exit(sys.exit)
    if open and format == 'html':
        webbrowser.open(str(build_dir / 'index.html'))


if __name__ == '__main__':
    main()
