import os
from pathlib import Path
from cli.config import DEFAULT_COMMIT


class Command:

    def __init__(self, igit):
        self.igit = igit

    def branch(self, branch_name=None):
        """
        Switch to another branch.
        :param branch_name: (optional) Branch name to switch to.
        """
        return self.igit.branch(branch_name)

    def add(self):
        # TODO - implement
        return 'NOT IMPLEMENTED'

    def commit(self):
        # TODO - implement
        return 'NOT IMPLEMENTED'

    def push(self):
        # TODO - implement
        return 'NOT IMPLEMENTED'

    def save(self, message=DEFAULT_COMMIT):
        """
        Adds and Commits changes.
        :param message: (optional) Commit message.
        """
        return self.igit.save(message)

    def up(self, message=DEFAULT_COMMIT):
        """
        Adds, Commits and Pushed changes to remote.
        :param message: (optional) Commit message.
        """
        return self.igit.up(message)

    def diff(self):
        """
        Prints diff of selected file.
        """
        return self.igit.diff()

    def undo(self, *scope):
        """
        Undo un-staged (non added) changes.
        :param optional file list as scope:
        """
        return self.igit.undo(scope)

    def regret(self, *scope):
        """
        Undo staged (added) changes.
        :param optional file list as scope:
        """
        return self.igit.regret(scope)

    def revert(self):
        # TODO - implement
        return 'NOT IMPLEMENTED'

    def rename(self, name):
        """
        Rename current branch.
        :param required new branch name:
        """
        return self.igit.rename(name)

    def ignore(self, opt=None):
        """
        Enable gitignore modifications: add, remove.
        Syncs gitignore to remote.
        """
        return self.igit.ignore(opt)

    def test(self):
        """
        Route for dev purposes
        """
        return self.igit.test()

    @staticmethod
    def version():
        here = Path(__file__).parent.absolute()
        package_conf = {}
        with open(os.path.join(here, "version.py")) as f:
            exec(f.read(), package_conf)
        return package_conf['__version__']
