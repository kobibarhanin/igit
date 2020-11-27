[![Build Status](https://travis-ci.com/kobibarhanin/gitenv.svg?branch=master)](https://travis-ci.com/kobibarhanin/igit)
[![PyPI version](https://badge.fury.io/py/igit.svg)](https://badge.fury.io/py/igit)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)
[![PyPI download month](https://img.shields.io/pypi/dm/igit.svg)](https://pypi.python.org/pypi/igit/)
[![Open Source Love svg1](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)


# Igit - Interactive Git

Igit is an interactive supplementary CLI to git for a better git experience.

<img src="https://github.com/kobibarhanin/igit/raw/master/examples/igit_preview.gif"
    width="600px" border="0" alt="igit_preview">

## The Story:

For a long time I've been using a variety of aliases for git commands, some of which were custom and aimed to boosting my git productivity - so I've decided to package it into a product for others to use.

## Main features:

🚀 **Fast commits** - add, commit & push, instantly.

↪️ **Undo changes** - cancel changes made to any file.

🦘 **Branch hopping** - move between branches, even if you have unstaged changes, without having to stage them.

⛔ **Easy ignore** - add files to ignore, use templates, fix remote sync.

🎹 **Interactivity** - selectors, checkboxes and prompts instead of typing.

## Installation

With [pip](https://pip.pypa.io/en/stable/):

```bash
pip install igit
```

## Usage

<img src="https://github.com/kobibarhanin/igit/raw/master/examples/help.png"
    width="450px" border="0" alt="help">

For a comprehensive user guide - visit igit's [wiki](https://github.com/kobibarhanin/igit/wiki/User-Guide).

## Compatibility

Igit is cross-platform → Windows, MacOSX, Linux.

🤓 - **Windows users will get best experience with Windows Terminal / WSL**.

## Built with

- [click](https://github.com/pallets/click)
- [gitpython](https://github.com/gitpython-developers/GitPython)
- [inquirer](https://github.com/CITGuru/PyInquirer)
- [rich](https://github.com/willmcgugan/rich)

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please make sure to update tests as appropriate.

### Local dev environment (MacOSX / Linux)

- Clone this project
- cd into project directory
- Run: pipenv install
- Run: pipenv --venv
- Add [bash alias](https://linuxize.com/post/how-to-create-bash-aliases/):

```bash
alias igit='PYTHONPATH=<LOCAL IGIT PROJECT DIR> <PIPENV VENV PATH>/bin/python3 <LOCAL IGIT PROJECT DIR>/igit/cli.py'
```

- Now you can run igit from bash and code changes in local igit dir will apply.

## License

[MIT](https://choosealicense.com/licenses/mit/)
