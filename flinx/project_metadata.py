"""Read the project metadata from a variety of sources."""

import re
import subprocess
import sys
from datetime import datetime
from functools import reduce
from pathlib import Path

import pytoml as toml

test_filename_re = re.compile(r'^(test_|_test)$')
version_re = re.compile(r'^\s*__version__\s*=\s*(\'.*?\'|".*?")', re.M)


class CombinedMetadata(object):
    """Combine metadata from multiple sources."""

    def __init__(self, sources):
        self.sources = sources

    def __getitem__(self, key):
        """Return a project metadata value."""
        for source in self.sources:
            try:
                return source[key]
            except KeyError:
                pass
        raise KeyError(key)


class PyProjectMetadataProviderABC(object):
    """Abstract base class for metadata sources that read ``pyproject.toml``."""

    _metadata = {}
    _translations = {}

    def __init__(self, project_path='pyproject.toml'):
        project = toml.loads(Path(project_path).read_text())
        try:
            dotpath = self._toml_path.split('.')
            self._metadata = reduce(lambda a, b: a[b], dotpath, project)
        except KeyError:
            pass

    def __getitem__(self, key):
        """Return a project metadata value."""
        translation = self._translations.get(key, key)
        if isinstance(translation, list):
            for k in translation:
                try:
                    return self[k]
                except KeyError:
                    pass
            raise KeyError(key)
        getter = getattr(self, '_get_' + translation.replace('-', '_'), None)
        if callable(getter):
            return getter()
        return self._metadata[translation]


class FlinxMetadata(PyProjectMetadataProviderABC):
    """Provide project metadata from the Flinx section of ``pyproject.toml``."""

    _toml_path = 'tool.flinx.metadata'


class FlitMetadata(PyProjectMetadataProviderABC):
    """Metadata provider that reads the Flit data from ``pyproject.toml``."""

    _toml_path = 'tool.flit.metadata'
    _translations = {
        'name': ['dist-name', 'module'],
        'readme': 'description-file',
    }


class PoetryMetadata(PyProjectMetadataProviderABC):
    """Provide project metadata from the Poetry section of ``pyproject.toml``."""

    _toml_path = 'tool.poetry'

    def _get_author(self):
        authors = self['authors']
        if not authors:
            raise KeyError('author')
        authors = [(author + '<').split('<')[0].strip() for author in authors]
        if len(authors) > 1:
            authors[-1] = 'and ' + authors[-1]
        return (', ' if len(authors) > 2 else ' ').join(authors)


def read_version_def(path):
    """Return the version string from a module."""
    match = version_re.search(path.read_text())
    return match.group(1).strip('"\'') if match else None


def module_candidates(project_path='.', search='file'):
    """Yield the candidate modules in the current directory.

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


class NoUniqueModuleError(Exception):
    """No module found."""

    pass


def find_module(project_home):
    """Find the module. Prefer directories over files."""
    module_paths = module_candidates(project_home, 'file') \
        or module_candidates(project_home, 'dir')
    if not module_paths:
        raise NoUniqueModuleError("Couldn't find module")
    if len(module_paths) > 1:
        raise NoUniqueModuleError("Too many module candidates")
    return Path(module_paths[0])


class InferredProjectMetadata(object):
    """Metadata provider that detects metadata from files in the current directory."""

    readme_re = re.compile(r'^README.(md|rst)$', re.I)

    def __init__(self, project_path='.'):
        self.project_path = Path(project_path)

    def _get_module(self):
        return str(find_module(self.project_path).name)

    def _get_name(self):
        return str(self.project_path.name)

    def _get_author(self):
        process = subprocess.run(["git", "config", "user.name"],
                                 stdout=subprocess.PIPE)
        if process.returncode:
            sys.exit(1)
        if not process.stdout:
            raise Exception("Couldn't detect user name")
        return process.stdout.decode().strip()

    def _get_date(self):
        return datetime.now().strftime('%Y')

    def _get_readme(self):
        paths = [path for path in self.project_path.glob("*")
                 if self.readme_re.match(str(path.name))]
        return str(paths[0].name) if paths else None

    def __getitem__(self, key):
        """Return a project metadata value."""
        fn = getattr(self, '_get_' + key, None)
        if not fn:
            raise KeyError(key)
        return fn()


class ProjectMetadata(CombinedMetadata):
    """Combine metadata from ``pyproject.toml`` and the directory structure."""

    _project_source_classes = [FlinxMetadata, FlitMetadata, PoetryMetadata]
    sources = []

    @classmethod
    def from_dir(cls, project_home):
        """Construct a ProjectMetadata that reads from the specified directory."""
        return cls(project_home)

    def __init__(self, project_home='.'):
        self._project_home = Path(project_home)
        project_file_path = self._project_home / 'pyproject.toml'
        sources = []
        if project_file_path.exists():
            sources += [cls(project_file_path) for cls in self._project_source_classes]
        sources.append(InferredProjectMetadata(self._project_home))
        super().__init__(sources)

    def _get_version(self):
        module_path = self._project_home / self['module']
        init_path = module_path / '__init__.py'
        path = init_path if module_path.is_dir() else Path(str(module_path) + '.py')
        return read_version_def(path)

    def __getitem__(self, key):
        """Return a project metadata value."""
        try:
            return super().__getitem__(key)
        except KeyError:
            if key == 'version':
                return self._get_version()
            raise


if __name__ == '__main__':
    for klass in [FlinxMetadata, FlitMetadata, PoetryMetadata,
                  InferredProjectMetadata, ProjectMetadata]:
        print(f'{klass.__name__}:')
        data = klass()
        for key in ['name', 'module', 'version', 'author', 'date', 'readme']:
            try:
                value = data[key]
                print("{:>8}: {}".format(key, value))
            except KeyError:
                pass
