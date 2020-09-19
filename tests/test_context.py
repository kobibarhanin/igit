from os import path
import fire

from cli.shell import run_cmd
from core.context import Context

from tests.fixtures.input_fixtures import test_dir, source_dir
from tests.fixtures.setup_fixtures import *


def test_init_context(gitsy_cmd, test_dir):
    fire.Fire(gitsy_cmd, command='init')
    context_branch = gitsy_cmd.gitsy.get_branch()
    print(f'{test_dir}/.gitsy/context_{context_branch}.yaml')
    assert path.exists(f'{test_dir}/.gitsy/context_{context_branch}.yaml')


def test_add_one_file_to_context(gitsy_ctx, test_file):
    cmd = gitsy_ctx
    fire.Fire(cmd, command=f'init')

    fire.Fire(cmd, command=f'add {test_file}')
    context = Context(cmd.gitsy.repo).get_context()

    assert context
    assert test_file in context['working-on']


def test_add_list_files_to_context(gitsy_ctx, test_files):
    cmd = gitsy_ctx
    fire.Fire(cmd, command=f'init')

    fire.Fire(cmd, command=f'add {" ".join(test_files)}')
    context = Context(cmd.gitsy.repo).get_context()

    assert context
    for file in test_files:
        assert file in context['working-on']


def test_change_undo(gitsy_ctx, test_file, test_dir):
    cmd = gitsy_ctx
    fire.Fire(cmd, command=f'init')

    # create a new file and stage it
    run_cmd(f'(cd {test_dir} && git add .)')

    # make changes to added file
    with open(f'{test_dir}/{test_file}', 'a') as f:
        f.write('test')

    print('\n======================================')
    # verify changes made to file
    res = run_cmd(f'(cd {test_dir} && git status)')
    assert f'modified:{test_file}' in str(res).replace(' ', '')

    fire.Fire(cmd, command=f'add {test_file}')

    print('======================================')
    # gitsy: undo changes to file and verify
    fire.Fire(cmd, command='undo all allow')
    res = run_cmd(f'(cd {test_dir} && git status)')
    assert f'modified:{test_file}' not in str(res).replace(' ', '')

    fire.Fire(cmd, command=f'clear')

    print('======================================')
    # gitsy: clean up all changes and verify
    fire.Fire(cmd, command='regret all allow')
    res = run_cmd(f'(cd {test_dir} && git status)')
    assert f'working tree clean' not in str(res).replace(' ', '')


def test_branch_selector():
    pass


def test_diff_selector():
    pass


def test_add_selector():
    pass
