import re
import subprocess
import sys
from pathlib import Path

import pytoml as toml

test_filename_re = re.compile(r'^(test_|_test)$')
version_re = re.compile(r'^\s*__version__\s*=\s*(\'.*?\'|".*?")', re.M)


class ProjectMetadata(object):
    """Return keyed metadata from the first successful provider."""

    sources = []

    @staticmethod
    def from_dir(dir):
        return ProjectMetadata(dir)

    def __init__(self, project_path='.'):
        path = Path(project_path) / 'pyproject.toml'
        if path.exists():
            self.sources += [FlitMetadata(path), PoetryMetadata(path)]
        self.sources.append(DetectedMetadata(project_path))

    def version(self):
        module_path = Path(self['module'])
        path = module_path / '__init__.py' \
            if module_path.is_dir() else Path(str(module_path)+'.py')
        return read_version_def(path)

    def __getitem__(self, key):
        if key == 'version':
            return self.version()
        for backer in self.sources:
            try:
                return backer[key]
            except KeyError:
                pass
        return KeyError(key)


class PyProjectMetadataProvider(object):
    _metadata = dict()
    _translations = {}

    def __init__(self, project_path='pyproject.toml'):
        try:
            project = toml.loads(Path(project_path).read_text())
        except FileNotFoundError:
            return
        from functools import reduce
        try:
            dotpath = self._toml_path.split('.')
            self._metadata = reduce(lambda a, b: a[b], dotpath, project)
        except KeyError:
            pass

    def __getitem__(self, key):
        if key in self._translations:
            key = self._translations[key]
        if callable(getattr(self, key, None)):
            return getattr(self, key)()
        return self._metadata[key]


class FlitMetadata(PyProjectMetadataProvider):
    """Metadata provider that reads the Flit data from ``pyproject.toml``."""

    _toml_path = 'tool.flit.metadata'
    _translations = {
        'name': 'module',
        'readme': 'description-file',
    }


class PoetryMetadata(PyProjectMetadataProvider):
    _toml_path = 'tool.poetry'

    def author(self):
        authors = self['authors']
        return (authors[0] + '<').split('<')[0] if authors else None


def read_version_def(path):
    match = version_re.search(path.read_text())
    return match.group(1).strip('"\'') if match else None


def modules_candidates(project_path='.', search='file'):
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


def find_module(project_path):
    """Find the module. Prefer directories over files."""
    module_paths = modules_candidates(project_path, 'file') or modules_candidates(project_path, 'dir')
    if not module_paths:
        raise Exception("Couldn't find a unique module")
    if len(module_paths) > 2:
        raise Exception("Too many module candidates")
    return module_paths[0]


class DetectedMetadata(object):
    """Metadata provider that detects metadata from files in the current directory."""

    def __init__(self, project_path='.'):
        self.project_path = Path(project_path)

    def module(self):
        return str(find_module(self.project_path))

    def author(self):
        process = subprocess.run(["git", "config", "user.name"],
                                 stdout=subprocess.PIPE)
        if process.returncode:
            sys.exit(1)
        if not process.stdout:
            raise Exception("Couldn't detect user name")
        return process.stdout.decode().strip()

    def readme(self):
        for filename in ['README.rst', 'README.md']:
            path = self.project_path / filename
            if path.exists():
                return str(path)
        return None

    def __getitem__(self, key):
        try:
            fn = getattr(self, key)
        except AttributeError:
            return IndexError(key)
        return fn()


if __name__ == '__main__':
    for klass in [FlitMetadata, PoetryMetadata, ProjectMetadata, DetectedMetadata]:
        print(f'{klass.__name__}:')
        data = klass()
        for key in ['module', 'version', 'author', 'readme']:
            try:
                value = data[key]
                print("{:>8}: {}".format(key, value))
            except KeyError:
                pass
