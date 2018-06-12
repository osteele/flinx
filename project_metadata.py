from pathlib import Path
import re

import pytoml as toml

test_filename_re = re.compile(r'^(test_|_test)$')
version_re = re.compile(r'^\s*__version__\s*=\s*(\'.*?\'|".*?")', re.M)


def read_version_def(path):
    version_str = version_re.search(path.read_text())
    return version_str[1].strip('"\'') if version_str else None


def modules_candidates(search='file'):
    """Yields the candidate modules in the current directory.

    A candidate file module is a non-test file that contains the string
    ``__version = …``, according to grep.

    A candidate directory module is a non-test directory that contains
    an ``__init__`` file that contains this string.

    ``search`` should be one of "file" and "dir".
    """
    if search == 'file':
        paths = [p for p in Path('.').glob('*.py') if p.is_file()]
        paths = [p for p in paths if not test_filename_re.match(str(p.stem))]
    else:
        paths = [p for p in Path('.').glob('*') if p.is_dir()]
        paths = [p / '__init__.py' for p in paths
                 if not test_filename_re.match(str(p))]
    paths = [p for p in paths if p.is_file()]
    paths = [p for p in paths if read_version_def(p)]
    if search == 'file':
        paths = [p.stem for p in paths]
    else:
        paths = [p.parent for p in paths]
    return paths


def find_module():
    """Find the module. Prefer directories over files."""
    module_paths = modules_candidates('file') or modules_candidates('dir')
    if not module_paths:
        raise Exception("Couldn't find a unique module")
    if len(module_paths) > 2:
        raise Exception("Too many module candidates")
    return module_paths[0]


class ComputedMetadata(object):
    def module(self):
        return str(find_module())

    def author(self):
        # TODO: git config, if present
        return 'Oliver Steele'

    def readme(self):
        for filename in ['README.rst', 'README.md']:
            if Path(filename).exists():
                return filename
        return None

    def __getitem__(self, key):
        try:
            fn = getattr(self, key)
        except AttributeError:
            return IndexError(key)
        return fn()


class PyProjectMetadata(object):
    _metadata = dict()
    _translation = {
        'readme': 'description-file',
    }

    def __init__(self):
        try:
            project = toml.load(open('pyproject.toml'))
            self._metadata = project['tool']['flit']['metadata']
        except (FileNotFoundError, KeyError):
            pass

    def __getitem__(self, key):
        if key in self._translation:
            key = self._translation[key]
        return self._metadata[key]


class MetadataConfig(object):
    backers = [PyProjectMetadata(), ComputedMetadata()]

    def version(self):
        module_path = Path(self['module'])
        path = module_path / '__init__.py' \
            if module_path.is_dir() else Path(str(module_path)+'.py')
        return read_version_def(path)

    def __getitem__(self, key):
        if key == 'version':
            return self.version()
        for backer in self.backers:
            try:
                return backer[key]
            except KeyError:
                pass
        return KeyError(key)
