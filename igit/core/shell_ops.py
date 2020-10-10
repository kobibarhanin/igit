import os
from invoke import run


class Shell:

    def __init__(self, silent=False, directory=None) -> None:
        self.silent = silent
        self.directory = directory

    def __rshift__(self, cmd):
        if self.directory:
            os.chdir(self.directory)
        result = run(cmd, hide=True, warn=True)
        if not result.ok:
            raise Exception(f'failed to run command: {cmd}\n'
                            f'{result.stderr}')
        if not self.silent:
            print(result.stdout)
        return result


if __name__ == "__main__":
    shell = Shell()
    shell >> "ls -la"
