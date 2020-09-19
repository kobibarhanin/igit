import os
import fire
import pytest

from cli.commands import Command
from core.gitsy import Gitsy

from tests.utils import random_str, file_name_prefix


__all__ = [
    'test_file',
    'test_files',
    'gitsy',
    'gitsy_cmd',
    'gitsy_ctx',
    'gitsy_global',
]


@pytest.fixture()
def gitsy(test_dir):
    gitsy = Gitsy(test_dir)
    return gitsy


@pytest.fixture()
def gitsy_cmd(gitsy):
    return Command(gitsy)


@pytest.fixture()
def gitsy_ctx(gitsy_cmd):
    fire.Fire(gitsy_cmd, command='init')
    yield gitsy_cmd
    fire.Fire(gitsy_cmd, command='clear')


@pytest.fixture()
def gitsy_global(gitsy_cmd, test_dir):
    yield gitsy_cmd


@pytest.fixture()
def test_file(test_dir):
    file_name = f'{file_name_prefix}_{random_str(5)}'
    open(f'{test_dir}/{file_name}', 'a').close()
    yield file_name
    os.remove(f'{test_dir}/{file_name}')


@pytest.fixture()
def test_files(test_dir):
    files = [f'{file_name_prefix}_{random_str(5)}' for _ in range(0, 5)]
    for file in files:
        open(f'{test_dir}/{file}', 'a').close()
    yield files
    for file in files:
        os.remove(f'{test_dir}/{file}')
