<!-- <p align="center"> -->

[![Build Status](https://travis-ci.com/kobibarhanin/gitenv.svg?branch=master)](https://travis-ci.com/kobibarhanin/igit)
[![PyPI version](https://badge.fury.io/py/igit.svg)](https://badge.fury.io/py/igit)

<!-- [![GitHub Stars](https://img.shields.io/github/stars/kobibarhanin/igit) -->

[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)
[![PyPI download month](https://img.shields.io/pypi/dm/ansicolortags.svg)](https://pypi.python.org/pypi/igit/)
[![Open Source Love svg1](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)

![GitHub stars](https://img.shields.io/github/stars/kobibarhanin/igit?style=social&label=Star&maxAge=2592000)
![GitHub forks](https://img.shields.io/github/forks/kobibarhanin/igit?style=social&label=Fork&maxAge=2592000)

# Igit - Interactive Git

Igit is an interactive supplementary CLI to git for better git experience.

<!-- ![help](examples/igit_preview.gif) -->
<p text-align="center">

<img src="https://github.com/kobibarhanin/igit/raw/master/examples/igit_preview.gif"
    width="600px" border="0" alt="bit">

</p>

## The Story:

For a long time I've been using a variety of aliases for git commands, some of which were custom and aimed to boosting my git productivity - so I've decided to package it into a product for others to use.

## Main features:

1. Fast commits - add, commit & push, instantly.
2. Undo changes - cancel changes made to any file.
3. Branch hopping - move between branches, even if you have unstaged changes, without having to stage them.
4. Easy ignore - add files to ignore, sync with remote.
5. Interactivity - select and check instead of typing.

## Installation

With [pip](https://pip.pypa.io/en/stable/):

```bash
pip install igit
```

## Usage

![help](examples/help.png)

For a comprehensive user guide - visit igit's [wiki](https://github.com/kobibarhanin/igit/wiki/User-Guide).

## Compatibility

igit is cross-platform → Windows, macOS, Linux.

🤓 - **Windows users will get best experience with Windows Terminal / WSL**.

## Built with

- click
- gitpython
- inquirer
- rich

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
alias igit='PYTHONPATH=<LOCAL GITSY PROJECT DIR> <PIPENV VENV PATH>/bin/python3 <LOCAL IGIT PROJECT DIR>/igit/cli.py'
```

- Now you can run igit from bash and code changes in local igit dir will apply.

## License

[MIT](https://choosealicense.com/licenses/mit/)
