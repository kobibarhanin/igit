import pytest
from cli.shell import run_cmd


__all__ = [
    'source_branch',
    'target_branch',
]


@pytest.fixture()
def source_branch(test_dir):
    run_cmd(f'(cd {test_dir} && git checkout state_a)')
    return 'state_a'


@pytest.fixture()
def target_branch(test_dir):
    return 'state_b'
