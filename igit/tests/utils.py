import random
import string


from pylint.lint import Run


file_name_prefix = 'file_'


def random_str(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def run_linter(module, pylintrc_path, threshold):
    lint_run = Run([module, f'--rcfile={pylintrc_path}'], exit=False)
    score = lint_run.linter.stats['global_note']
    assert score > threshold, f'FAILED: linting score for module {module} too low: {score}'
