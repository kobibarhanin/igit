import os
from os.path import join
from pathlib import Path
import copy

import yaml
from git import Repo

from cli.config import BRANCH_CONTEXT, GLOBAL_CONTEXT
from cli.display import display_message, display_list
from cli.interactive import files_checkboxes, verify_prompt

from core.gitcmd import in_gitignore, add_gitignore


def contextual(func):
    def context_wrapper(self, *args, **kwargs):
        if not os.path.exists(self.context_file):
            if verify_prompt('No context found for this branch, create one?'):
                self.init_context()
            else:
                return False
        context = self.get_context()
        res = func(self, context, *args, **kwargs)
        self._update_context(context)
        return res
    return context_wrapper


class Context:

    def __init__(self, repo) -> None:
        self.repo = repo
        self.repo_path = os.path.dirname(repo.git_dir)
        self.branch = repo.active_branch.name
        self.gitsy_path = join(self.repo_path, '.gitsy')
        self.context_file = join(self.gitsy_path, f'context_{self.branch}.yaml')

    # == CONSTRUCTORS ==========================================

    @classmethod
    def from_gitsy(cls, repo):
        return cls(repo)

    @classmethod
    def from_command(cls, cmd_path=os.getcwd()):
        repo = Repo(cmd_path, search_parent_directories=True)
        return cls(repo)

    # == END CONSTRUCTORS ==========================================

    def init_context(self):
        # TODO - prompt verify for actions:
        #  adding .gitsy dir, changing gitignore, commiting locally

        # create .gitsy dir, if needed
        gitsy_dir = join(self.repo_path, '.gitsy')
        if not os.path.isdir(gitsy_dir):
            os.mkdir(gitsy_dir)

        # add .gitsy to .gitignore, if needed
        try:
            gitignore_path = os.path.join(self.repo_path, '.gitignore')
            if not in_gitignore(gitignore_path, '.gitsy/'):
                add_gitignore(gitignore_path, '.gitsy/')
                self.repo.git.add('.gitignore')
                self.repo.git.commit('-m', 'gitsy init - update gitignore')
        except Exception as e:
            print(f'unable to add gitsy root to gitignore: {e}')

        # create context file
        if not os.path.exists(self.context_file):
            display_message(f'initiating local context for branch: {self.branch}', 'green', 'house')
            with open(self.context_file, 'w') as f:
                yaml.dump(BRANCH_CONTEXT, f)
        else:
            display_message(f'local context exists for branch: {self.branch}', 'yellow', 'house')

    def get_context(self, ignore_disabled=False):
        if os.path.exists(self.context_file):
            with open(self.context_file, 'r') as f:
                context = yaml.load(f, Loader=yaml.FullLoader)
                if ignore_disabled:
                    return context
                elif context['status'] == 'disabled':
                    global_context = copy.deepcopy(GLOBAL_CONTEXT)
                    global_context['local'] = True
                    return global_context
                else:
                    return context
        else:
            return GLOBAL_CONTEXT

    def status(self):
        """
        Prints:
            🏠 - Running in branch context: state_a
            📒 - Status: enabled
            👷 - working-on:
	                data4.txt
        """

        ctx = self.get_context()

        if ctx['type'] == 'branch':
            msg = f'Running in branch context: {self.branch}'
            icon = 'house'
        elif ctx['type'] == 'global':
            msg = f'Running in global context'
            msg += f' (disabled - {self.branch})' if ctx["local"] else ''
            icon = 'earth_africa'
        display_message(msg, 'magenta', icon)

        if ctx['type'] == 'branch':
            display_message(f'Status: {ctx["status"]}', 'green', 'ledger')
            if len(ctx["working-on"]) > 0:
                display_list('working-on', ctx['working-on'])
            else:
                display_message(f'No files in context', 'yellow', 'construction_worker')

    @contextual
    def add(self, context, files):
        if len(files) == 0:
            path = Path(self.repo_path)
            # collect all files in repo
            opt_files = [str(file.relative_to(self.repo_path))
                         for file in list(path.rglob('*'))
                         if self._file_conditions(self.repo_path, file)]
            # subtract files that are already added
            opt_files = set(opt_files) - set(context['working-on'])
            if not opt_files:
                return 'No files found to add.'
            else:
                files = files_checkboxes(list(opt_files), 'add')
        added_files = []
        for file in files:
            added_files.append(self._normalize_path(self.repo_path, file))
        added_files = set(added_files) - set(context['working-on'])
        context['working-on'] += list(added_files)
        display_list('added', added_files)

    def remove(self):
        if os.path.exists(self.context_file):
            os.remove(self.context_file)
            display_message(f'context for: {self.branch} deleted', 'green', 'ledger')
        else:
            display_message(f'context not found for: {self.branch}', 'yellow', 'ledger')

    @contextual
    def clear(self, context):
        context['working-on'].clear()
        display_message(f'context cleared', 'green', 'ledger')

    @contextual
    def rm(self, context, files):
        if len(files) == 0:
            if len(context["working-on"]) > 0:
                files = files_checkboxes(context['working-on'], 'remove from context')
            else:
                display_message(f'No files in context', 'yellow', 'construction_worker')
                return
        for file in list(files):
            context['working-on'].remove(file)
        display_list('removed', list(files))

    @contextual
    def disable(self, context):
        context['status'] = 'disabled'

    def enable(self):
        context = self.get_context(ignore_disabled=True)
        context['status'] = 'enabled'
        self._update_context(context)

    # == INTERNAL AUX METHODS ==================================

    def _update_context(self, context):
        with open(self.context_file, 'w') as f:
            yaml.dump(context, f)

    @staticmethod
    def _file_conditions(root, file):
        file_parents = [p.name for p in list(file.relative_to(root).parents)]
        return file.is_file() \
               and '.git' not in file_parents \
               and '.gitsy' not in file_parents

    @staticmethod
    def _file_dir_conditions(root, file):
        file_parents = [p.name for p in list(file.relative_to(root).parents)]
        return '.git' not in file_parents \
               and '.gitsy' not in file_parents

    @staticmethod
    def _normalize_path(repo_path, file):
        if not os.path.exists(join(repo_path, file)):
            rel_path = os.path.relpath(os.getcwd(), repo_path)
            adjusted_file = join(rel_path, file)
            return adjusted_file
        else:
            return file

    # == END INTERNAL AUX METHODS ==============================
