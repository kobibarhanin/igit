import os
from pathlib import Path

import click

from igit.core.commands import Igit


@click.group()
def cli():
    """
    Interactive Git for better git experience.
    """
    pass


@cli.command(help='add unstaged files')
@click.option('--file', default=[], help='file to add', multiple=True)
@click.option('--all', '-a', is_flag=True, default=False, help='add all unstaged files')
def add(file, all):
    Igit().add(file, all)


@cli.command(help='commit changes')
@click.option('--message', '-m', default=None, help='commit message')
@click.option('--add', '-a', is_flag=True, default=False, help='add before commit')
def commit(message, add):
    Igit().commit(message, add)


@cli.command(help='push changes')
@click.option('--add', '-a', is_flag=True, default=False, help='add --all and commit before push')
@click.option('--commit', '-c', is_flag=True, default=False, help='push to remote')
def push(add, commit):
    Igit().push(add, commit)


@cli.command(help='Adds and Commits changes')
@click.option('--message', default=None, help='commit message (optional)')
def save(message):
    Igit().save(message)


@cli.command(help='Adds, Commits and Pushes changes to remote')
@click.option('--message', default=None, help='commit message (optional)')
def up(message):
    Igit().up(message)


@cli.command(help='Switch to another branch')
@click.option('--name', '-n', default=None, help='target branch to switch to')
@click.option('--hopping_on', '-h', is_flag=True, default=False, help='activate branch hopping')
def branch(name, hopping_on):
    return Igit().branch(name, hopping_on)


@cli.command(help='Prints diff of selected file')
def diff():
    return Igit().diff()


@cli.command(help='Undo un-staged (non added) changes')
@click.option('--file', default=[], help='file to add', multiple=True)
@click.option('--all', is_flag=True, default=False, help='undo all unstaged changes')
def undo(file, all):
    return Igit().undo(file, all)


@cli.command(help='Unstage changes')
@click.option('--file', default=[], help='file to add', multiple=True)
@click.option('--all', is_flag=True, default=False, help='unstage all files')
def unstage(file, all):
    return Igit().unstage(file, all)


@cli.command(help='revert commit (NOT IMPLEMENTED)')
def revert():
    # TODO - implement
    return 'NOT IMPLEMENTED'


@cli.command(help='Rename current branch')
@click.argument('name')
def rename(name):
    return Igit().rename(name)


@cli.command(help='Perform .gitignore modifications: add, remove, sync with remote, etc.')
@click.option('--reset', is_flag=True, default=False, help='resets gitignore')
def ignore(reset):
    return Igit().ignore(reset)


@cli.command(help='Print igit version')
def version():
    here = Path(__file__).parent.absolute()
    package_conf = {}
    with open(os.path.join(here, "__version__.py")) as f:
        exec(f.read(), package_conf)
    print(package_conf['__version__'])


if __name__ == "__main__":
    try:
        cli(prog_name='igit')
    except Exception as e:
        print(e)
