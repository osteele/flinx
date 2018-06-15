from flinx.project_metadata import (FlinxMetadata, FlitMetadata, InferredProjectMetadata,
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
    for name, value in expected_metadata.items():
        assert metadata[name] == value


def test_flit_metadata():
    metadata = FlitMetadata('./tests/files/pyproject.toml')
    for name, value in expected_metadata.items():
        if name != 'version':
            assert metadata[name] == value


def test_poetry_metadata():
    metadata = PoetryMetadata('./tests/files/pyproject.toml')
    for name, value in expected_metadata.items():
        if name != 'module':
            assert metadata[name] == value


def test_metadata_discovery():
    metadata = InferredProjectMetadata('./tests/files/one-file')
    assert metadata['name'] == 'one-file'
    assert metadata['module'] == 'file-1'
    assert metadata['readme'] == 'README.rst'

    metadata = InferredProjectMetadata('./tests/files/one-folder')
    assert metadata['name'] == 'one-folder'
    assert metadata['readme'] == 'README.md'
    # assert metadata['module'] == 'folder-1'

    metadata = InferredProjectMetadata('./tests/files/file-and-folder')
    assert metadata['name'] is not None
    assert metadata['readme'] == 'readme.md'

    metadata = InferredProjectMetadata('./tests/files/no-valid-file')
    # TODO: this should raise an error

    metadata = InferredProjectMetadata('./tests/files/two-files')
    assert metadata['name'] is not None
    assert metadata['readme'] is None

    metadata = InferredProjectMetadata('./tests/files/two-versioned-files')
    # TODO: this should raise an error

    metadata = ProjectMetadata.from_dir('./tests/files/one-file')
    assert metadata['version'] == '1.0.0'
