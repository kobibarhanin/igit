import os

from git import Repo
from git import InvalidGitRepositoryError
from git import GitCommandError
from termcolor import colored

from cli.shell import run_cmd
from cli.display import *
from cli.interactive import *
from cli.config import *

from core.context import Context
from core.config import DIFF_MAP
from core.gitcmd import in_gitignore, add_gitignore


class Gitsy:

    def __init__(self, repo_path=os.getcwd()):
        try:
            # initialize repo object
            self.repo = Repo(repo_path, search_parent_directories=True)
            self.repo_path = os.path.dirname(self.repo.git_dir)

            # initialize attributes for methods usage
            self._cwd = os.getcwd()
            self._branch = self.repo.active_branch.name

            self.context = Context.from_gitsy(self.repo)

        except InvalidGitRepositoryError:
            raise Exception('Not a git repo, I have no power here...')

    def get_branch(self):
        return self._branch

    # ====================== NON CONTEXTUAL METHODS =====================

    def branch(self, target_branch):
        """
        Swith to target_branch if specified, else prompt branch menu.
        Implements auto-stashing to allow flex branch hopping.
        :param target_branch:
        :return:
        """
        if not target_branch:
            branches = [branch.name for branch in list(self.repo.branches)]
            if len(branches) == 1:
                return 'No local branches detected'
            else:
                target_branch = branch_selector(branches)
                if not target_branch:
                    return

        # handle branch hopping in case of untracked files
        untracked = self.repo.untracked_files
        if untracked:
            display_list_no_icon('Untracked files found', 'white', untracked)
            if not verify_prompt(f'Stage them to continue?'):
                display_message('Stage files to branch with gitsy', 'yellow', 'sweat_smile')
                return
            else:
                display_message('Staging untracked files', 'yellow', 'floppy_disk')
                self.repo.git.add(untracked)

        change_list = self._calculate_change_list(GLOBAL_CONTEXT,
                                                  diff_types=['unstaged', 'staged'])

        if len(change_list) > 0:
            self.repo.git.stash(f'save', f'{GLOBAL_STASH_PREFIX}_{self.get_branch()}')
            display_message(f'Saving diff (stash): {GLOBAL_STASH_PREFIX}_{self.get_branch()}', 'green', 'thumbsup')
        self._switch_branch(target_branch)

        stash_list = self.repo.git.stash('list')
        stash_stub = f'{GLOBAL_STASH_PREFIX}_{self.get_branch()}'
        if stash_list:
            stash_list = stash_list.split("\n")

        for stash in stash_list:
            stash_name = stash.split(' ')[-1]
            if stash_stub == stash_name:
                stash_index = stash.split(' ')[0].replace(':', '')
                self.repo.git.stash(f'pop', stash_index)
                display_message(f'Loading diff (stash): {stash_name}', 'green', 'thumbsup')
                break

    def rename(self, name):
        try:
            self.repo.active_branch.rename(name)
            context = self.context.get_context(ignore_disabled=True)
            if context['type'] == 'branch':
                os.rename(self.context.context_file,
                          os.path.join(self.context.gitsy_path, f'context_{name}.yaml'))
        except Exception as e:
            print(e)

    # TODO - sub cmds: add, remove, list, reset
    def ignore(self, opt):
        if opt is None:
            # TODO - code duplication for add to context
            from pathlib import Path
            path = Path(self.repo_path)
            # collect all files in repo
            opt_files = [str(file.relative_to(self.repo_path))
                         for file in list(path.rglob('*'))
                         if self.context._file_dir_conditions(self.repo_path, file)]
            # subtract files that are already added
            if not opt_files:
                return 'No files found to add.'
            else:
                files = files_checkboxes(list(opt_files), 'add')
                if files:
                    try:
                        gitignore_path = os.path.join(self.repo_path, '.gitignore')
                        for file in files:
                            if not in_gitignore(gitignore_path, file):
                                add_gitignore(gitignore_path, file)
                    except Exception as e:
                        print(f'No gitignore file found: {e}')
                else:
                    display_message('gitignore unchanged (use space key to select!)', 'yellow', 'speak_no_evil')

        elif opt == 'reset':
            # self.repo.index.remove('.', '-r')
            run_cmd('git rm -r --cached .')
            run_cmd('git add .')
            run_cmd('git commit -m ".gitignore fixed"')

    # ====================== OPTIONALLY CONTEXTUAL METHODS =====================

    def up(self, message):
        context = self.context.get_context()
        change_list = self._calculate_change_list(context,
                                                  diff_types=['unstaged', 'staged'])
        if change_list:
            self._up(change_list, message)
        else:
            ctx = 'global' if context['type'] == 'global' else self.get_branch()
            msg = f'Nothing to send up within context: {ctx}'
            display_message(msg, 'yellow', 'speak_no_evil')

    def save(self, message):
        context = self.context.get_context()
        change_list = self._calculate_change_list(context,
                                                  diff_types=['unstaged'])
        if change_list:
            self._save(change_list, message)
        else:
            return f'No changes to save within context: {self._branch}'

    def diff(self):
        context = self.context.get_context()
        change_list = self._calculate_change_list(context,
                                                  diff_types=['unstaged'])
        if not change_list:
            ctx = 'global' if context['type'] == 'global' else self.get_branch()
            msg = f'No diff found within context: {ctx}'
            display_message(msg, 'yellow', 'speak_no_evil')
            return

        file = file_selector(change_list)
        if not file:
            return
        diffs = self.repo.git.diff(file).split('\n')
        for diff in diffs:
            display_diff(diff)

    def undo(self, scope):
        context = self.context.get_context()
        try:
            scope = self._get_scope(context, scope, 'undo', diff_types=['unstaged'])
        except Exception as e:
            return e
        if scope:
            self.repo.git.checkout('--', list(scope))
            display_list('undo', scope)

    def regret(self, scope):
        context = self.context.get_context()
        try:
            scope = self._get_scope(context, scope, 'regret', diff_types=['staged'])
        except Exception as e:
            return e
        self.repo.git.reset('--', scope)
        display_list('unstaged', scope)

    # ==================== INTERNAL AUX METHODS ====================

    def _up(self, files, message):
        try:
            self._save(files, message)
            display_list('up', files)
        except GitCommandError:
            print(colored(f'pushing without changes', 'cyan'))
        self.repo.git.push('origin', self._branch)
        display_message('pushed', 'green', 'thumbsup')

    def _save(self, files, message):
        display_list('saving', files)
        self.repo.git.add(files)
        commit = self.repo.git.commit('-m', message)
        display_message(commit, 'white', 'cat')
        display_message('saved', 'green', 'thumbsup')

    def _switch_branch(self, branch_name):
        self.repo.git.checkout(branch_name)
        self._branch = self.repo.active_branch.name
        display_message(f'Switched to branch: {self._branch}', 'yellow', 'checkered_flag')

    def _get_scope(self, context, scope, method, diff_types):
        change_list = self._calculate_change_list(context, diff_types)
        if len(scope) == 0:
            if len(change_list) > 0:
                scope = files_checkboxes(change_list, method)
            else:
                # TODO - ugly code, this issue was seen in other places, need to generalize actions within context type (branch / global)
                raise Exception(f'No actionable items found in {context["type"]} context{"." if context["type"] == "global" else ": " + self._branch}')
        elif scope[0] == 'all':
            if len(scope) < 2 or not scope[1] == 'allow':
                if not verify_prompt(f'This will {method} all staged changes'):
                    return
            scope = change_list
        else:
            scope = [value for value in scope
                     if value in change_list]
        return scope

    def _calculate_change_list(self, context, diff_types=None):
        change_list = []
        for diff_type in diff_types:
            change_list += [item.a_path for item
                            in self.repo.index.diff(DIFF_MAP[diff_type])]
        change_list += self.repo.untracked_files

        context_list = context['working-on'] if context['type'] == 'branch' else change_list
        return self._intersection(change_list, context_list)

    @staticmethod
    def _intersection(iterable1, iterable2):
        return list(set(iterable1).intersection(iterable2))

    # ==================== TEST METHODS ====================

    def test(self):
        print('=== TEST ROUTE ===')
        print(self.branch)
        print('=== END TEST ROUTE ===')
