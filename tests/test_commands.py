from pathlib import Path
from unittest.mock import patch

import flinx.commands as commands

from click.testing import CliRunner


@patch('sys.exit')
@patch('webbrowser.open')
@patch('flinx.commands.sphinx_build')
@patch('flinx.commands.write_template_files')
def test_build(write_template_files, sphinx_build, wb_open, sys_exit):
    runner = CliRunner()
    result = runner.invoke(commands.cli, ['build'])
    assert result.exit_code == 0
    assert result.output == ''
    write_template_files.assert_called_with(Path('docs'), force=False, unless_exists=False, verbose=False)
    sphinx_build.assert_called_with(['-b', 'html', '-c', 'docs', '-j', 'auto', '-q',
                                     'docs', 'docs/_build/html'])
    wb_open.assert_not_called()
    sys_exit.assert_called_with(0)

    sphinx_build.reset_mock()
    write_template_files.reset_mock()
    result = runner.invoke(commands.cli, ['build', '--format', 'pdf'])
    assert result.exit_code == 0
    sphinx_build.assert_called_once()
    assert sphinx_build.call_args[0][0][:2] == ['-b', 'pdf']

    sphinx_build.reset_mock()
    write_template_files.reset_mock()
    result = runner.invoke(commands.cli, ['build', '--open-url'])
    assert result.exit_code == 0
    wb_open.assert_called_once()

    sphinx_build.reset_mock()
    write_template_files.reset_mock()
    result = runner.invoke(commands.cli, ['build', '--verbose'])
    assert result.exit_code == 0
    sphinx_build.assert_called_once()
    assert '-q' not in sphinx_build.call_args[0][0]


@patch('sys.exit')
@patch('flinx.commands.sphinx_build')
@patch('flinx.commands.build_sphinx_args')
@patch('flinx.commands.write_template_files')
def test_build_options(write_template_files, build_sphinx_args, sphinx_build, sys_exit):
    runner = CliRunner()
    runner.invoke(commands.cli, ['build'])
    build_sphinx_args.assert_called_with(all_files=False, force=False, fmt='html',
                                         open_url=False, unless_exists=False,
                                         verbose=False)

    build_sphinx_args.reset_mock()
    runner.invoke(commands.cli, ['build', '--unless-exists'])
    build_sphinx_args.assert_called_with(all_files=False, force=False,
                                         fmt='html', open_url=False,
                                         unless_exists=True, verbose=False)


@patch('sys.exit')
@patch('subprocess.run')
@patch('flinx.commands.build_sphinx_args', return_value={
    'build_args': ['--build-args--'],
    'build_dir': '_build',
    'docs_dir': 'docs',
})
def test_serve(build_sphinx_args, subprocess_run, sys_exit):
    runner = CliRunner()

    result = runner.invoke(commands.cli, ['serve'])
    assert result.exit_code == 0
    assert result.output == ''
    subprocess_run.assert_called_with(['sphinx-autobuild', '--build-args--'])
    sys_exit.assert_called_with(0)

    result = runner.invoke(commands.cli, ['serve', '--open-url'])
    assert result.exit_code == 0
    assert result.output == ''
    subprocess_run.assert_called_with(['sphinx-autobuild', '--build-args--', '-B'])
    sys_exit.assert_called_with(0)


def test_files_exist():
    runner = CliRunner()
    with runner.isolated_filesystem():
        Path('module.py').write_text('__version__ = "0.1.0"\n')

        result = runner.invoke(commands.cli, ['generate'])
        assert result.exit_code == 0
        assert 'Wrote docs/conf.py' in result.output
        assert 'Wrote docs/index.rst' in result.output

        result = runner.invoke(commands.cli, ['generate'])
        assert result.exit_code == 0, "can overwrite a generated file"

        result = runner.invoke(commands.cli, ['eject'])
        assert result.exit_code == 0

        result = runner.invoke(commands.cli, ['generate'])
        assert result.exit_code == 1, "can't overwrite a non-generated file"

        result = runner.invoke(commands.cli, ['generate', '--unless-exists'])
        assert result.exit_code == 0, "no error when --unless-exists"

        result = runner.invoke(commands.cli, ['generate'])
        assert result.exit_code == 1, "--unless-exists leaves the non-generated file"

        result = runner.invoke(commands.cli, ['generate', '--force'])
        assert result.exit_code == 0, "no error when --force"

        result = runner.invoke(commands.cli, ['generate'])
        assert result.exit_code == 0, "--force overwrites the non-generated file"
