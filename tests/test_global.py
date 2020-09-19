import fire

from cli.shell import run_cmd
from cli.config import GLOBAL_STASH_PREFIX

from tests.fixtures.input_fixtures import test_dir, source_dir
from tests.fixtures.state_fixtures import source_branch, target_branch
from tests.fixtures.setup_fixtures import *


def test_ignore(gitsy_cmd, test_dir, source_branch, target_branch):
    pass


def test_branch(gitsy_cmd, test_dir, source_branch, target_branch):
    cmd = gitsy_cmd
    # make changes at source branch and verify
    run_cmd(f'(cd {test_dir} && ./make_changes.sh 1)')
    change_list = [item.a_path for item in cmd.gitsy.repo.index.diff(None)]
    assert len(change_list) > 0

    # move to target branch, verify branch, verify stashed changes
    fire.Fire(cmd, command=f'branch {target_branch}')
    assert cmd.gitsy.get_branch() == target_branch
    assert run_cmd(f'git stash list | grep {GLOBAL_STASH_PREFIX}_{source_branch}')[2] == 0

    run_cmd('git add .')  # this is needed for handling unstaged files in .gitsy folder

    # make changes at target branch and verify
    run_cmd(f'(cd {test_dir} && ./make_changes.sh 2)')
    change_list = [item.a_path for item in cmd.gitsy.repo.index.diff(None)]
    assert len(change_list) > 0

    run_cmd('git add .')  # this is needed for handling unstaged files in .gitsy folder

    # move back to source branch, verify branch, verify stashed from target branch, verify stash stack
    fire.Fire(cmd, command=f'branch {source_branch}')
    assert cmd.gitsy.get_branch() == source_branch
    assert run_cmd(f'git stash list | grep {GLOBAL_STASH_PREFIX}_{source_branch}')[2] == 1
    assert run_cmd(f'git stash list | grep {GLOBAL_STASH_PREFIX}_{target_branch}')[2] == 0

    # verify original changes are restated
    change_list = [item.a_path for item in cmd.gitsy.repo.index.diff(None)]
    assert len(change_list) > 0
