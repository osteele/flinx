import re
import subprocess
import sys
from datetime import datetime
from functools import reduce
from pathlib import Path

import pytoml as toml

test_filename_re = re.compile(r'^(test_|_test)$')
version_re = re.compile(r'^\s*__version__\s*=\s*(\'.*?\'|".*?")', re.M)


class PyProjectMetadataProviderABC(object):
    _metadata = dict()
    _translations = {}

    def __init__(self, project_path='pyproject.toml'):
        project = toml.loads(Path(project_path).read_text())
        try:
            dotpath = self._toml_path.split('.')
            self._metadata = reduce(lambda a, b: a[b], dotpath, project)
        except KeyError:
            pass

    def __getitem__(self, key):
        if key in self._translations:
            key = self._translations[key]
        if isinstance(key, list):
            for k in key:
                try:
                    return self[k]
                except KeyError:
                    pass
            raise KeyError(key)
        if callable(getattr(self, key, None)):
            return getattr(self, key)()
        return self._metadata[key]


class FlinxMetadata(PyProjectMetadataProviderABC):
    _toml_path = 'tool.flinx.metadata'


class FlitMetadata(PyProjectMetadataProviderABC):
    """Metadata provider that reads the Flit data from ``pyproject.toml``."""

    _toml_path = 'tool.flit.metadata'
    _translations = {
        'name': ['dist-name', 'module'],
        'readme': 'description-file',
    }


class PoetryMetadata(PyProjectMetadataProviderABC):
    _toml_path = 'tool.poetry'

    def author(self):
        authors = self['authors']
        if not authors:
            raise KeyError('author')
        authors = [(author + '<').split('<')[0].strip() for author in authors]
        if len(authors) > 1:
            authors[-1] = 'and ' + authors[-1]
        return (', ' if len(authors) > 2 else ' ').join(authors)


def read_version_def(path):
    match = version_re.search(path.read_text())
    return match.group(1).strip('"\'') if match else None


def module_candidates(project_path='.', search='file'):
    """Yields the candidate modules in the current directory.

    A candidate file module is a non-test file that contains the string
    ``__version = …``, according to grep.

    A candidate directory module is a non-test directory that contains
    an ``__init__`` file that contains this string.

    ``search`` should be one of "file" and "dir".
    """
    root = Path(project_path)
    if search == 'file':
        paths = [p for p in root.glob('*.py') if p.is_file()]
        paths = [p for p in paths if not test_filename_re.match(str(p.stem))]
    else:
        paths = [p for p in root.glob('*') if p.is_dir()]
        paths = [p / '__init__.py' for p in paths
                 if not test_filename_re.match(str(p))]
        paths = [p for p in paths if p.is_file()]
    paths = [p for p in paths if read_version_def(p)]
    if search == 'file':
        paths = [p.stem for p in paths]
    else:
        paths = [p.parent for p in paths]
    return paths


class NoModuleException(Exception):
    pass


def find_module(project_path):
    """Find the module. Prefer directories over files."""
    module_paths = module_candidates(project_path, 'file') \
        or module_candidates(project_path, 'dir')
    if not module_paths:
        raise NoModuleException("Couldn't find module")
    if len(module_paths) > 2:
        raise NoModuleException("Too many module candidates")
    return module_paths[0]


class InspectedMetadata(object):
    """Metadata provider that detects metadata from files in the current directory."""

    readme_re = re.compile(r'^README.(md|rst)$', re.I)

    def __init__(self, project_path='.'):
        self.project_path = Path(project_path)

    def module(self):
        return str(find_module(self.project_path))

    def name(self):
        return str(self.project_path.name)

    def author(self):
        process = subprocess.run(["git", "config", "user.name"],
                                 stdout=subprocess.PIPE)
        if process.returncode:
            sys.exit(1)
        if not process.stdout:
            raise Exception("Couldn't detect user name")
        return process.stdout.decode().strip()

    def date(self):
        return datetime.now().strftime('%Y')

    def readme(self):
        paths = [path.name for path in self.project_path.glob("*")
                 if self.readme_re.match(str(path.name))]
        return str(paths[0]) if paths else None

    def __getitem__(self, key):
        try:
            fn = getattr(self, key)
        except AttributeError:
            raise KeyError(key)
        return fn()


class CombinedMetadata(object):
    """Return keyed metadata from the first successful source."""

    def __init__(self, sources):
        self.sources = sources

    def __getitem__(self, key):
        for source in self.sources:
            try:
                return source[key]
            except KeyError:
                pass
        raise KeyError(key)


class ProjectMetadata(CombinedMetadata):
    _project_sources = [FlinxMetadata, FlitMetadata, PoetryMetadata]
    sources = []

    @classmethod
    def from_dir(klass, dir):
        return klass(dir)

    def __init__(self, dir='.'):
        self._dir = Path(dir)
        project_path = self._dir / 'pyproject.toml'
        sources = []
        if project_path.exists():
            sources += [klass(project_path) for klass in self._project_sources]
        sources.append(InspectedMetadata(dir))
        super().__init__(sources)

    def _get_version(self):
        module_path = self._dir / self['module']
        path = module_path / '__init__.py' \
            if module_path.is_dir() else Path(str(module_path)+'.py')
        return read_version_def(path)

    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        except KeyError:
            if key == 'version':
                return self._get_version()
            raise


if __name__ == '__main__':
    for klass in [FlinxMetadata, FlitMetadata, PoetryMetadata,
                  InspectedMetadata, ProjectMetadata]:
        print(f'{klass.__name__}:')
        data = klass()
        for key in ['name', 'module', 'version', 'author', 'date', 'readme']:
            try:
                value = data[key]
                print("{:>8}: {}".format(key, value))
            except KeyError:
                pass
