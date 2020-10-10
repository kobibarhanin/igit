import os
import pytest
from click.testing import CliRunner


from igit.core.commands import Igit
from igit.core.shell_ops import Shell
from igit.cli import add, unstage, undo, commit


@pytest.fixture()
def source_dir():
    return os.environ['source_dir']


@pytest.fixture()
def test_dir():
    return os.environ['test_dir']


@pytest.fixture()
def igit(test_dir):
    return Igit(test_dir)


def test_add(igit):
    shell = Shell(directory=igit.gitops.repo_path)
    shell >> "./make_changes.sh 2"
    unstaged_files = len(igit.gitops.get_changed_files('unstaged'))
    assert unstaged_files == 1

    runner = CliRunner()
    result = runner.invoke(add, ['--all'])
    assert result.exit_code == 0

    unstaged_files = len(igit.gitops.get_changed_files('unstaged'))
    assert unstaged_files == 0
    staged_files = len(igit.gitops.get_changed_files('staged'))
    assert staged_files == 1

    # clean up - unstage
    result = runner.invoke(unstage, ['--all'])
    assert result.exit_code == 0
    staged_files = len(igit.gitops.get_changed_files('staged'))
    assert staged_files == 0

    # clean up - undo
    result = runner.invoke(undo, ['--all'])
    assert result.exit_code == 0
    unstaged_files = len(igit.gitops.get_changed_files('unstaged'))
    assert unstaged_files == 0


def test_commit(igit):
    shell = Shell(directory=igit.gitops.repo_path)
    shell >> "./make_changes.sh 2"
    unstaged_files = len(igit.gitops.get_changed_files('unstaged'))
    assert unstaged_files == 1

    runner = CliRunner()
    result = runner.invoke(add, ['--all'])
    assert result.exit_code == 0

    unstaged_files = len(igit.gitops.get_changed_files('unstaged'))
    assert unstaged_files == 0
    staged_files = len(igit.gitops.get_changed_files('staged'))
    assert staged_files == 1

    result = runner.invoke(commit, ['-m', 'test commit'])
    assert result.exit_code == 0

    staged_files = len(igit.gitops.get_changed_files('staged'))
    assert staged_files == 0
    unstaged_files = len(igit.gitops.get_changed_files('unstaged'))
    assert unstaged_files == 0
