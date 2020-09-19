import os
from pathlib import Path
from cli.config import DEFAULT_COMMIT


class Command:

    def __init__(self, gitsy):
        self.gitsy = gitsy

    #  == Git operations commands ========

    def branch(self, branch_name=None):
        """
        Switch to another branch.
        :param branch_name: (optional) Branch name to switch to.
        """
        return self.gitsy.branch(branch_name)

    def up(self, message=DEFAULT_COMMIT):
        """
        Adds, Commits and Pushed changes to remote.
        :param message: (optional) Commit message.
        """
        return self.gitsy.up(message)

    def save(self, message=DEFAULT_COMMIT):
        """
        Adds and Commits changes.
        :param message: (optional) Commit message.
        """
        return self.gitsy.save(message)

    def diff(self):
        """
        Prints diff of selected file.
        """
        return self.gitsy.diff()

    def undo(self, *scope):
        """
        Undo un-staged (non added) changes.
        :param optional file list as scope:
        """
        return self.gitsy.undo(scope)

    def regret(self, *scope):
        """
        Undo staged (added) changes.
        :param optional file list as scope:
        """
        return self.gitsy.regret(scope)

    def rename(self, name):
        """
        Rename current branch.
        :param required new branch name:
        """
        return self.gitsy.rename(name)

    def ignore(self, opt=None):
        """
        Enable gitignore modifications: add, remove.
        Syncs gitignore to remote.
        """
        return self.gitsy.ignore(opt)

    def test(self):
        """
        Route for dev purposes
        """
        return self.gitsy.test()

    # == Context operations commands ========

    def init(self):
        """
        Creates .gitsy directory if not yet created
        Adds .gitsy path to gitignore if not yet added
        Creates context file for current branch.
        """
        return self.gitsy.context.init_context()

    def context(self):
        """
        Prints current context information.
        """
        return self.gitsy.context.status()

    def add(self, *files):
        return self.gitsy.context.add(files)

    def rm(self, *files):
        return self.gitsy.context.rm(files)

    def clear(self):
        return self.gitsy.context.clear()

    def remove(self):
        return self.gitsy.context.remove()

    def disable(self):
        return self.gitsy.context.disable()

    def enable(self):
        return self.gitsy.context.enable()

    # == General commands ===================

    @staticmethod
    def version():
        here = Path(__file__).parent.absolute()
        package_conf = {}
        with open(os.path.join(here, "version.py")) as f:
            exec(f.read(), package_conf)
        return package_conf['__version__']
