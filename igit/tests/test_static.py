from igit.tests.test_main import source_dir
from igit.tests.utils import run_linter


def test_linting(source_dir):
    run_linter('igit.core', f'{source_dir}/tests/.pylintrc', 8)
    run_linter('igit.interactive', f'{source_dir}/tests/.pylintrc', 8)
