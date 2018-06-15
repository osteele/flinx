import pytest
from flinx.project_metadata import (FlinxMetadata, FlitMetadata,
                                    InferredProjectMetadata, NoUniqueModuleError,
                                    PoetryMetadata, ProjectMetadata)

expected_metadata = {
    'name': 'project-name',
    'module': 'module-name',
    'version': '1.0.0',
    'author': 'Oliver Steele',
    'readme': './README.rst',
}


def test_flinx_metadata():
    metadata = FlinxMetadata('./tests/files/pyproject.toml')
    assert metadata['name'] == 'project-name'
    assert metadata['module'] == 'module-name'
    assert metadata['version'] == '1.0.0'
    assert metadata['author'] == 'Oliver Steele'
    assert metadata['readme'] == './README.rst'


def test_flit_metadata():
    metadata = FlitMetadata('./tests/files/pyproject.toml')
    assert metadata['name'] == 'project-name'
    assert metadata['module'] == 'module-name'
    # no 'version'
    assert metadata['author'] == 'Oliver Steele'
    assert metadata['readme'] == './README.rst'


def test_poetry_metadata():
    metadata = PoetryMetadata('./tests/files/pyproject.toml')
    assert metadata['name'] == 'project-name'
    # no 'module'
    assert metadata['version'] == '1.0.0'
    assert metadata['author'] == 'Oliver Steele'
    assert metadata['readme'] == './README.rst'


def test_metadata_discovery():
    metadata = InferredProjectMetadata('./tests/files/one-file')
    assert metadata['name'] == 'one-file'
    assert metadata['module'] == 'file-1'
    assert metadata['readme'] == 'README.rst'
    # TODO: metadata['version'] should raise an exception

    metadata = InferredProjectMetadata('./tests/files/one-folder')
    assert metadata['name'] == 'one-folder'
    assert metadata['module'] == 'folder-1'
    assert metadata['readme'] == 'README.md'

    metadata = InferredProjectMetadata('./tests/files/file-and-folder')
    assert metadata['name'] is not None
    assert metadata['module'] == 'file-1'
    assert metadata['readme'] == 'readme.md'

    metadata = InferredProjectMetadata('./tests/files/no-valid-file')
    with pytest.raises(NoUniqueModuleError):
        metadata['module']

    metadata = InferredProjectMetadata('./tests/files/two-files')
    assert metadata['name'] is not None
    assert metadata['module'] == 'file-1'
    assert metadata['readme'] is None

    metadata = InferredProjectMetadata('./tests/files/two-versioned-files')
    with pytest.raises(NoUniqueModuleError):
        metadata['module']

    metadata = ProjectMetadata.from_dir('./tests/files/one-file')
    assert metadata['module'] == 'file-1'
    assert metadata['version'] == '1.0.0'
