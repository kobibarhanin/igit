import os
from pathlib import Path

import requests
from git import InvalidGitRepositoryError
from git import GitCommandError

from igit.core.fs_ops import get_files
from igit.interactive.display import Display
from igit.interactive.interact import Interact
from igit.core.shell_ops import Shell
from igit.core.config import *

from igit.core.git_ops import in_gitignore, add_gitignore, GitOps


class Igit:

    def __init__(self, path=os.getcwd()):
        try:
            self.gitops = GitOps(path)
            self.display = Display()
            self.interact = Interact()
        except InvalidGitRepositoryError:
            raise

    def add(self, _files, _all):
        try:
            unstaged = self.gitops.get_changed_files('unstaged') + \
                       self.gitops.get_untracked_files()
            if unstaged:
                if _all:
                    selected = unstaged
                elif _files:
                    selected = self._intersection(_files, unstaged)
                else:
                    selected = self.interact.choose('choose files to add', unstaged)
                if selected:
                    self.gitops.repo.git.add(selected)
                    self.display.list('added', selected, 'green', 'thumbsup')
                else:
                    self.display.message('command had no effect', 'yellow', 'speak_no_evil')
            else:
                self.display.message('nothing to add', 'yellow', 'speak_no_evil')
        except GitCommandError as e:
            self.display.message(f'unable to add\n{e}', 'red', 'x')

    def commit(self, _message, _add):
        if not _message:
            prompt = self.interact.text(f'commit message [{DEFAULT_COMMIT}]')
            _message = prompt if prompt else DEFAULT_COMMIT
        if _add:
            self.add(_files=None, _all=True)
        try:
            if len(self.gitops.repo.index.diff("HEAD")) > 0:
                commit_resp = self.gitops.repo.git.commit('-m', _message)
                self.display.message(commit_resp, 'white', 'cat')
                self.display.message('committed', 'yellow', 'lock')
            else:
                self.display.message('nothing to commit', 'yellow', 'lock')
        except GitCommandError as e:
            self.display.message(f'unable to commit\n{e}', 'red', 'x')

    def push(self, _add, _commit):
        if _add:
            self.add(_files=None, _all=False)
            self.commit(_message=None, _add=False)
        elif _commit:
            self.commit(_message=None, _add=True)
        try:
            self.gitops.repo.git.push('origin', self.gitops.branch)
            self.display.message('pushed', 'cyan', 'rocket')
        except GitCommandError as e:
            self.display.message(f'unable to push\n{e}', 'red', 'x')

    def save(self, message):
        self.add(_files=None, _all=True)
        message = message if message else DEFAULT_COMMIT
        self.commit(_message=message, _add=False)

    def up(self, message, commit, add):                
        self.add(_files=None, _all=False if add else True)
        self.commit(_message=None if commit else message if message else DEFAULT_COMMIT, _add=False)
        self.push(_add=False, _commit=False)

    def branch(self, target_branch, hopping_mode, create_new, migrate_mode):
        """
        Swith to target_branch if specified, else prompt branch menu.
        Implements auto-stashing to allow flex branch hopping.
        :param target_branch:
        :return:
        """
        if migrate_mode:
            carry_stash = f'{GLOBAL_STASH_PREFIX}_{self.gitops.branch}'
            print(self.gitops.repo.git.stash(f'save', carry_stash))
            

        if create_new:
            branch_name = Interact().text('Give it a name')
            self.gitops.create_branch(branch_name)
            return

        if not target_branch:
            branches = [branch.name for branch in list(self.gitops.repo.branches)]
            if len(branches) == 1:
                create_new = Interact().confirm('No local branches detected. create new?')
                if create_new:
                    branch_name = Interact().text('Give it a name')
                    if migrate_mode:
                        stash_list = self.gitops.repo.git.stash('list')
                        stash_stub = carry_stash
                        if stash_list:
                            stash_list = stash_list.split("\n")
                            for stash in stash_list:
                                stash_name = stash.split(' ')[-1]
                                if stash_stub == stash_name:
                                    stash_index = stash.split(' ')[0].replace(':', '')
                                    self.gitops.repo.git.stash(f'pop', stash_index)
                                    self.display.message(f'Loading diff (stash): {stash_name}', 'green', 'thumbsup')
                                    break
                    self.gitops.create_branch(branch_name)
                    return
                return
            else:
                target_branch = self.interact.select('choose terget branch', ['[New]'] + branches)
                if not target_branch:
                    return
                if target_branch == '[New]':
                    if migrate_mode:
                        stash_list = self.gitops.repo.git.stash('list')
                        stash_stub = carry_stash
                        if stash_list:
                            stash_list = stash_list.split("\n")
                            for stash in stash_list:
                                stash_name = stash.split(' ')[-1]
                                if stash_stub == stash_name:
                                    stash_index = stash.split(' ')[0].replace(':', '')
                                    self.gitops.repo.git.stash(f'pop', stash_index)
                                    self.display.message(f'Loading diff (stash): {stash_name}', 'green', 'thumbsup')
                                    break
                    branch_name = Interact().text('Give it a name')
                    self.gitops.create_branch(branch_name)
                    return

        if hopping_mode:
            # handle branch hopping in case of untracked files
            untracked = self.gitops.get_untracked_files()
            if untracked:
                self.display.list('Untracked files found', untracked, 'white', 'speak_no_evil')
                if not self.interact.confirm(f'Stage them to continue?'):
                    self.display.message('Stage files to branch with igit', 'yellow', 'sweat_smile')
                    return
                else:
                    self.display.message('Staging untracked files', 'yellow', 'floppy_disk')
                    self.gitops.repo.git.add(untracked)

            change_list = self.gitops.get_all_changes()

            if len(change_list) > 0:
                self.gitops.repo.git.stash(f'save', f'{GLOBAL_STASH_PREFIX}_{self.gitops.branch}')
                self.display.message(f'Saving diff (stash): {GLOBAL_STASH_PREFIX}_{self.gitops.branch}', 'green', 'thumbsup')

        self.gitops.switch_branch(target_branch)

        if hopping_mode:
            stash_list = self.gitops.repo.git.stash('list')
            stash_stub = f'{GLOBAL_STASH_PREFIX}_{self.gitops.branch}'
            if stash_list:
                stash_list = stash_list.split("\n")

            for stash in stash_list:
                stash_name = stash.split(' ')[-1]
                if stash_stub == stash_name:
                    stash_index = stash.split(' ')[0].replace(':', '')
                    self.gitops.repo.git.stash(f'pop', stash_index)
                    self.display.message(f'Loading diff (stash): {stash_name}', 'green', 'thumbsup')
                    break

    def diff(self):
        change_list = self.gitops.get_changed_files('unstaged')
        if not change_list:
            self.display.message('No diff found', 'yellow', 'speak_no_evil')

        file = self.interact.select('select file to view diff', change_list)
        if not file:
            return
        diffs = self.gitops.repo.git.diff(file).split('\n')
        for diff in diffs:
            self.display.diff(diff)

    def rename(self, name):
        try:
            # TODO - interactivize
            self.gitops.repo.active_branch.rename(name)
        except Exception as e:
            print(e)

    def undo(self, _files, _all):
        try:
            unstaged = self.gitops.get_changed_files('unstaged')
            if unstaged:
                if _all:
                    selected = unstaged
                elif _files:
                    selected = self._intersection(_files, unstaged)
                else:
                    selected = self.interact.choose('choose files to undo changes', unstaged)
                if selected:
                    self.gitops.repo.git.checkout('--', selected)
                    self.display.list('changes undone', selected, 'green', 'thumbsup')
                else:
                    self.display.message('command had no effect', 'yellow', 'speak_no_evil')
            else:
                self.display.message('nothing to undo', 'yellow', 'speak_no_evil')
        except GitCommandError as e:
            self.display.message(f'unable to undo\n{e}', 'red', 'x')

    def unstage(self, _files, _all):
        try:
            unstaged = self.gitops.get_changed_files('staged')
            if unstaged:
                if _all:
                    selected = unstaged
                elif _files:
                    selected = self._intersection(_files, unstaged)
                else:
                    selected = self.interact.choose('choose files to unstage', unstaged)
                if selected:
                    self.gitops.repo.git.reset('--', selected)
                    self.display.list('files unstaged', selected, 'green', 'thumbsup')
                else:
                    self.display.message('command had no effect', 'yellow', 'speak_no_evil')
            else:
                self.display.message('nothing to unstage', 'yellow', 'speak_no_evil')
        except GitCommandError as e:
            self.display.message(f'unable to unstage\n{e}', 'red', 'x')

    def revert(self, commit):
        if commit:
            self.gitops.repo.head.reset(commit, index=True)
        else:
            self.gitops.repo.head.reset('HEAD~1', index=True)
            # FOR HARD RESET:
            # self.gitops.repo.head.reset('HEAD~1', index=True, working_tree=True)

    def ignore(self, reset, create):
        # check for .gitignore file, prompt to create if none detected
        gitignore_path = os.path.join(self.gitops.repo_path, '.gitignore')

        if create:
            self.gitops.create_gitignore(gitignore_path)
            return

        if not os.path.exists(gitignore_path):
            if self.interact.confirm('no gitignore file detected, create new?'):
                self.gitops.create_gitignore(gitignore_path)

        if reset:
            shell = Shell()
            shell >> 'git rm -r --cached .'
            self.commit('.gitignore fixed by igit', True)

        else:
            ex_dirs = [Path(ex_dir) for ex_dir in ['.git']]
            opt_files = get_files(Path(self.gitops.repo_path), ex_dirs, [], False)
            opt_files = [str(file) for file in opt_files]

            # subtract files that are already added
            if not opt_files:
                return 'No files found to add.'
            else:
                files = self.interact.choose('select files to gitignore', opt_files)
                if files:
                    try:
                        for file in files:
                            if not in_gitignore(gitignore_path, file):
                                add_gitignore(gitignore_path, file)
                    except Exception as e:
                        print(f'No gitignore file found: {e}')
                else:
                    self.display.message('gitignore unchanged (use space key to select!)', 'yellow', 'speak_no_evil')


    @staticmethod
    def _intersection(iterable1, iterable2):
        return list(set(iterable1).intersection(iterable2))
