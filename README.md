[![Build Status](https://travis-ci.com/kobibarhanin/gitenv.svg?branch=master)](https://travis-ci.com/kobibarhanin/gitenv)
[![PyPI version](https://badge.fury.io/py/gitsy.svg)](https://badge.fury.io/py/gitsy)

# Gitsy - Git made easy!

| NOTICE: gitsy is still very much under construction, I'll notify when a standard beta version is ready. |
| --- |

Gitsy is a supplementary CLI to git for better git flow and productivity.

## Main features:
1. Fast commits - one-stop-shop for git's add, commit and push. 
2. Undo changes - easily undo all changes made to a file, whether it was staged or unstaged.
3. Easy branch hopping - move between branches, even if you have unstaged changes, without having to stage them.
4. Simplify git ignore resetting - that annoying thing where you accidentally pushed something you wanted ignored. 
5. Interactiveness - gitsy incorporates selectable lists, checkboxes and prompt to enhance git
6. Contextual - gitsy supplies a kind of git environment, based on the active branch, ...


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install gitsy:

```bash
pip install gitsy
```

## Usage
gitsy can be used in a globaly with no context (out-of-the-box) or in a branch context.

### No context:

```bash
# git add .
# git commit -m "commit message"
# git push 

# IS NOW:
gitsy up "commit message" 

# Notes:
# - Commit message is optional (defaulted to 'fast commit').
# - Auto handles the case of setting remote origin for new branches.
```
![Alt text](examples/images/gitsy_up.png?raw=true "Title")
```bash
# To undo changes in an unstaged changed file:
gitsy undo file_1.py 
# To pick a file just drop the file's name:
gitsy undo
```
![Alt text](examples/images/gitsy_undo.png?raw=true "Title")
```bash

# for staged files use:
gitsy regret

# ... 
```

### Branch context:

- TBD

## Compatibility
gitsy is designed to be a cross-platform product, and therefore is supported on Windows, macOS and Linux.
- windows users will get best experience with windows terminal (powershell session).


## Built with

- google-fire
- gitpython
- inquirer
- emoji

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please make sure to update tests as appropriate.

### Local dev environment (macOS / Linux)

- Clone this project
- cd into project directory
- Run: pipenv install
- Run: pipenv --venv 
- Add [bash alias](https://linuxize.com/post/how-to-create-bash-aliases/):
```bash
alias gitsy='PYTHONPATH=<LOCAL GITSY PROJECT DIR> <PIPENV VENV PATH>/bin/python3 <LOCAL GITSY PROJECT DIR>/entrypoint/entrypoint.py'
```
- Now you can run gitsy from bash and code changes in local gitsy dir will apply.


## License
[MIT](https://choosealicense.com/licenses/mit/)
