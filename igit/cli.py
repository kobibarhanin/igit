import os
from pathlib import Path

import click
from click_help_colors import HelpColorsGroup
from git import InvalidGitRepositoryError

from igit.core.commands import Igit
from igit.interactive.display import Display


@click.group(
    cls=HelpColorsGroup,
    help_headers_color='yellow',
    help_options_color='magenta',
    help_options_custom_colors={
        'up': 'cyan',
        'push': 'cyan',
        'undo': 'red',
        'unstage': 'red',
        'revert': 'red',
        'diff': 'green',
        'branch': 'green',
        'add': 'blue',
        'commit': 'blue',
        'save': 'blue',
    }
)
def cli():
    """\b
_____        __________
___(_)______ ___(_)_  /_
__  /__  __ `/_  /_  __/
_  / _  /_/ /_  / / /_
/_/  _\__, / /_/  \__/
     /____/
    """


@cli.command(
    help='Add unstaged files.'
)
@click.option('--file', default=[], help='file to add', multiple=True)
@click.option('--all', '-a', is_flag=True, default=False, help='add all unstaged files')
def add(file, all):
    Igit().add(file, all)


@cli.command(help='Commit changes.')
@click.option('--message', '-m', default=None, help='commit message')
@click.option('--add', '-a', is_flag=True, default=False, help='add before commit')
def commit(message, add):
    Igit().commit(message, add)


@cli.command(help='Adds and Commits changes.')
@click.option('--message', default=None, help='commit message (optional)')
def save(message):
    Igit().save(message)


@cli.command(help='Adds, Commits and Pushes changes to remote.')
@click.option('--add', '-a', is_flag=True, default=False, help='prompts for staging files')
@click.option('--commit', '-c', is_flag=True, default=False, help='prompts for commit message')
@click.option('--message', '-m', default=None, help='commit message (optional)')
@click.option('--interactive', '-i', is_flag=True, default=False, help='alias for --add --commit')
def up(message, commit, add, interactive):
    if interactive:
        Igit().up(None, True, True)
    else:    
        Igit().up(message, commit, add)


@cli.command(help='Switch to another branch.')
@click.option('--name', '-n', default=None, help='target branch to switch to')
@click.option('--hop', '-h', is_flag=True, default=False, help='activate branch hopping')
@click.option('--create', '-c', is_flag=True, default=False, help='create a new branch')
def branch(name, hop, create):
    return Igit().branch(name, hop, create)


@cli.command(help='Prints diff of selected file.')
def diff():
    return Igit().diff()


@cli.command(help='Undo un-staged (non added) changes.')
@click.option('--file', default=[], help='file to add', multiple=True)
@click.option('--all', is_flag=True, default=False, help='undo all unstaged changes')
def undo(file, all):
    return Igit().undo(file, all)


@cli.command(help='Unstage changes.')
@click.option('--file', default=[], help='file to add', multiple=True)
@click.option('--all', is_flag=True, default=False, help='unstage all files')
def unstage(file, all):
    return Igit().unstage(file, all)


@cli.command(help='Revert last commit.')
@click.option('--commit', '-c', default=None, help='commit hash to revert')
def revert(commit):
    return Igit().revert(commit)


@cli.command(help='Rename current branch.')
@click.argument('name')
def rename(name):
    return Igit().rename(name)


@cli.command(help='Perform .gitignore operations.')
@click.option('--reset', is_flag=True, default=False, help='resets gitignore')
@click.option('--create', is_flag=True, default=False, help='create gitignore filr from template')
def ignore(reset, create):
    return Igit().ignore(reset, create)


@cli.command(help='Prints igit version.')
def version():
    here = Path(__file__).parent.absolute()
    package_conf = {}
    with open(os.path.join(here, "__version__.py")) as f:
        exec(f.read(), package_conf)
    print(package_conf['__version__'])


def run():
    try:
        cli(prog_name='igit')
    except InvalidGitRepositoryError as e:
        Display().message(e, 'yellow', 'sweat_smile')
    except Exception as e:
        Display().message(f'Encountered an error: {e}', 'red', 'x')


if __name__ == "__main__":
    run()
