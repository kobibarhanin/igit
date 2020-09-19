import os
import fire
from dotenv import load_dotenv

from cli.commands import Command
from core.gitsy import Gitsy


load_dotenv()


def main():
    try:
        # running in dev mode from pycharm
        if 'PC' in os.environ:
            cmd = input('enter command: ') or 'add'
            fire.Fire(Command(Gitsy(os.getenv('test_dir'))), command=cmd)
        else:
            fire.Fire(Command(Gitsy()))
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
