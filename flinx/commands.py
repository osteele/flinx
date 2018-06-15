"""Flinx CLI."""

import inspect
import subprocess
import sys
import webbrowser
from functools import reduce, wraps
from pathlib import Path

import click
import pytoml as toml
from jinja2 import Environment

from sphinx.cmd.build import main as sphinx_build

from .project_metadata import NoModuleError, ProjectMetadata

GENERATED_TEXT = "THIS FILE IS AUTOMATICALLY GENERATED BY FLINX. "
"MANUAL CHANGES WILL BE LOST."

# Allow these names as shortcuts for sphinx.ext.*.
sphinx_builtin_extensions = ['autodoc', 'autosectionlabel', 'autosummary', 'coverage',
                             'doctest', 'extlinks', 'githubpages', 'graphviz',
                             'ifconfig', 'imgconverter',
                             'imgmath', 'mathjax', 'jsmith', 'inheritance_diagram',
                             'intersphinx', 'linkcode', 'napoleon', 'todo', 'viewcode']

# Configuration variables that start with image_ imply the imgconverter (not image)
# extension, etc.
config_var_ext_prefixes = {'image': 'imgconverter', 'inheritance': 'inheritance_graph'}

# Use this, if the user doesn't specify extensions.
default_extensions = ['autodoc']

env = Environment()
env.filters['repr'] = repr
poject_relpath = Path('..')
env.filters['project_rel'] = lambda s: str(poject_relpath / s)

TEMPLATE_DIR = Path(__file__).parent / 'templates'
conf_tpl = env.from_string((TEMPLATE_DIR / 'conf.py.tpl').read_text())
index_tpl = env.from_string((TEMPLATE_DIR / 'index.rst.tpl').read_text())


def write_template_files(output_dir, include_generated_warning=True, verbose=True):
    """Generate the ``conf.py`` and ``README.rst`` files."""
    # TODO: refuse to overwrite non-generated files?
    metadata = ProjectMetadata.from_dir('.')
    config = get_sphinx_configuration('.')
    try:
        metadata['name']  # for effect
    except NoModuleError as e:
        sys.stderr.write("{}\n".format(e))
        sys.exit(1)
    generated_text = GENERATED_TEXT if include_generated_warning else None
    index_text = index_tpl.render(
        readme=metadata['readme'],
        module_name=metadata['module'],
        generated_text=generated_text,
    )
    index_path = output_dir / 'index.rst'
    index_path.write_text(index_text)
    if verbose:
        print('wrote', index_path)

    author = metadata['author']
    copyright_year = metadata['date']
    config['extensions'] = get_extensions(config)
    conf_text = conf_tpl.render(
        module_path='..',
        project=metadata['name'],
        copyright=f'{copyright_year}, {author}',
        author=author,
        version=metadata['version'],
        source_suffix=['.rst'],
        master_basename='index',
        generated_text=generated_text,
        config=config.items(),
    )
    conf_path = output_dir / 'conf.py'
    conf_path.write_text(conf_text)
    if verbose:
        print('wrote', conf_path)
    return conf_path


def get_extensions(config_vars):
    """Infer the extensions from the Sphinx configuration variables."""
    # expand shortcut names
    extensions = ['sphinx.ext.' + ext
                  if ext in sphinx_builtin_extensions else ext
                  for ext in config_vars.get('extensions', default_extensions)]
    # add extensions implied by configuration value names
    prefixes = {k.split('_', 1)[0] for k in config_vars.keys() if '_' in k}
    detected_exts = (config_var_ext_prefixes.get(prefix, prefix)
                     for prefix in prefixes)
    auto_exts = sorted('sphinx.ext.' + ext
                       for ext in detected_exts
                       if ext in sphinx_builtin_extensions)
    for ext in auto_exts:
        if ext not in extensions:
            extensions.append(ext)
    return extensions


def get_sphinx_configuration(project_dir):
    """Read the Sphinx configuration from ``pyproject.toml```."""
    try:
        project = toml.loads((Path(project_dir) / 'pyproject.toml').read_text())
        return reduce(lambda a, b: a[b], 'tool.flinx.configuration'.split('.'), project)
    except (FileNotFoundError, KeyError):
        return {}


@click.group()
def cli():
    """Configuration-free Sphinx builder."""
    pass


@cli.command()
def generate():
    """Write the generated files."""
    docs_dir = Path('./docs')
    write_template_files(docs_dir, verbose=True)


@cli.command()
def eject():
    """Write the generated files, without header warnings."""
    docs_dir = Path('./docs')
    write_template_files(docs_dir, include_generated_warning=False, verbose=True)


def build_sphinx_args(all_files=False, format='html', verbose=False, **args):
    """Translate shared options into a new set of options, and write templates."""
    docs_dir = Path('./docs')
    build_dir = docs_dir / '_build' / format
    docs_dir.mkdir(exist_ok=True)
    conf_path = write_template_files(docs_dir, verbose=verbose)
    args = [
        '-b', format,
        '-c', str(conf_path.parent),  # config file
        '-j', 'auto',  # processors
        '-q',  # quiet
        str(docs_dir),
        str(build_dir)
    ]
    if all_files:
        args += ['-a']
    return dict(build_args=args, build_dir=build_dir, docs_dir=docs_dir)


def with_sphinx_build_args(f):
    """Decorate a function to consume a common set of options."""
    @click.option('-a', '--all-files', is_flag=True,
                  help='Rebuild all the docs, regardless of what has changed.')
    @click.option('-o', '--open-url', is_flag=True,
                  help='Open the HTML index in a browser.')
    @click.option('--format', default='html', type=click.Choice(['html']),
                  help='The output format.')
    @click.option('--verbose', is_flag=True)
    @wraps(f)
    def wrapper(**kwargs):
        # build_args, build_dir, docs_dir = build_sphinx_args(**kwargs)
        build_args = build_sphinx_args(**kwargs)
        kwargs = {k: v for k, v in kwargs.items() if k not in consumed_args}
        for k, v in build_args.items():
            if k in wrapped_args:
                kwargs[k] = v
        return f(**kwargs)

    def position_param_names(f):
        var_parameter_kinds = \
            (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD)
        return {p.name for p in inspect.signature(f).parameters.values()
                if p.kind not in var_parameter_kinds}

    wrapped_args = position_param_names(f)
    consumed_args = position_param_names(build_sphinx_args) - wrapped_args
    return wrapper


@cli.command()
@with_sphinx_build_args
def build(build_args=None, docs_dir=None, build_dir=None, format=None, open_url=False):
    """Use sphinx-build to build the documentation."""
    status = sphinx_build(build_args)
    if status:
        sys.exit(sys.exit)
    if open_url and format == 'html':
        webbrowser.open(str(build_dir / 'index.html'))


@cli.command()
@with_sphinx_build_args
def serve(build_args=None, open_url=False):
    """Use sphinx-autobuild to build and serve the documentation."""
    if open_url:
        build_args += ['-B']
    process = subprocess.run(['sphinx-autobuild'] + build_args)
    if process.returncode:
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(cli() or 0)
