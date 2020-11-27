<p align="center">

<a href="#"><img src="https://img.shields.io/github/stars/kobibarhanin/igit?style=social&label=Star&maxAge=2592000" alt="github stars"></a>

<h1>Igit - Interactive Git</h1>

Igit is an interactive supplementary CLI to git for better git experience.

    <img 
    src="https://github.com/kobibarhanin/igit/raw/master/examples/igit_preview.gif"
    width="600px" border="0" alt="bit">
</p>

<!-- ![help](examples/igit_preview.gif) -->

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
