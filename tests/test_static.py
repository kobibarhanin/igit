from tests.fixtures.input_fixtures import source_dir
from tests.utils import run_linter


def test_linting(source_dir):
    run_linter('core', f'{source_dir}/tests/.pylintrc', 7)
    run_linter('cli', f'{source_dir}/tests/.pylintrc', 5)
