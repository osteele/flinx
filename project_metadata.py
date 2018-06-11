import pytoml as toml


class ComputedMetadata(object):
    def module(self):
        # TODO: look for a folder that contains an __init__.py
        return 'flinx'

    def author(self):
        # TODO: git config, if present
        return 'Oliver Steele'

    def readme(self):
        for filename in ['README.rst', 'README.md']:
            if Path(filename).exists():
                return filename
        return None

    def version(self):
        # TODO: read from package
        return '0.1.0'

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

    def __getitem__(self, key):
        for backer in self.backers:
            try:
                return backer[key]
            except KeyError:
                pass
        return KeyError(key)
