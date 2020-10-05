import os
from pathlib import Path
from igit.core.config import DEFAULT_COMMIT
from igit.core.commands import Igit
import click


@click.group()
def cli():
    pass


@cli.command()
@click.option('--name', default=None, help='target branch to switch to')
@click.option('--hopping_on', is_flag=True, default=False, help='activate branch hopping')
def branch(name, hopping_on):
    """
    Switch to another branch.
    """
    return Igit().branch(name, hopping_on)


@cli.command()
def add():
    Igit().add()


@cli.command()
def commit():
    # TODO - implement
    return 'NOT IMPLEMENTED'


@cli.command()
def push():
    # TODO - implement
    return 'NOT IMPLEMENTED'


@cli.command()
@click.option('--message', default=DEFAULT_COMMIT, help='commit message')
def save(message):
    """
    Adds and Commits changes.
    :param message: (optional) Commit message.
    """
    igit = Igit()
    return igit.save(message)


@cli.command()
@click.option('--message', default=DEFAULT_COMMIT, help='commit message')
def up(message):
    """
    Adds, Commits and Pushed changes to remote.
    :param message: (optional) Commit message.
    """
    return Igit().up(message)


@cli.command()
def diff():
    """
    Prints diff of selected file.
    """
    return Igit().diff()


@cli.command()
@click.option('--scope', default=[], help='list files to undo')
def undo(*scope):
    """
    Undo un-staged (non added) changes.
    :param optional file list as scope:
    """
    return Igit().undo(scope)


@cli.command()
@click.option('--scope', default=[], help='list files to regret')
def regret(*scope):
    """
    Undo staged (added) changes.
    :param optional file list as scope:
    """
    return Igit().regret(scope)


@cli.command()
def revert():
    # TODO - implement
    return 'NOT IMPLEMENTED'


@cli.command()
# @click.option('--name', default='', help='Who are you?')
def rename(name):
    """
    Rename current branch.
    :param required new branch name:
    """
    return Igit().rename(name)


@cli.command()
@click.option('--opt', default=None, help='todo - ignore operations')
def ignore(opt=None):
    """
    Enable gitignore modifications: add, remove.
    Syncs gitignore to remote.
    """
    return Igit().ignore(opt)


@cli.command()
# @click.option('--name', default='', help='Who are you?')
def test():
    """
    Route for dev purposes
    """
    return Igit().test()


@cli.command()
def version():
    here = Path(__file__).parent.absolute()
    package_conf = {}
    with open(os.path.join(here, "__version__.py")) as f:
        exec(f.read(), package_conf)
    print(package_conf['__version__'])


if __name__ == "__main__":
    try:
        cli()
    except Exception as e:
        print(e)
