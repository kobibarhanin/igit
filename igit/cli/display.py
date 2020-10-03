import os
import emoji
from emoji import EMOJI_ALIAS_UNICODE
from termcolor import colored

__all__ = ['display_list', 'display_message', 'display_list_no_icon', 'display_diff']

os_type = os.name

# COLORS:
# -------
# 'grey'    - not usable
# 'red'     - failure
# 'green'   - success
# 'blue'    - selectors
# 'magenta' - context
# 'yellow'  - local actions
# 'cyan'    - remote actions
# 'white'   - standard (git returns)

# ICONS:
# ------
# https://www.webfx.com/tools/emoji-cheat-sheet/

colors = {
    'saving': 'yellow',
    'saved': 'green',
    'pushed': 'green',
    'up': 'cyan',
    'undo': 'green',
    'unstaged': 'green',
    'added': 'magenta',
    'working-on': 'cyan',
    'status': 'magenta',
    'removed': 'magenta',
}


icons = {
    'saving': ':floppy_disk:',
    'saved': ':thumbsup:',
    'pushed': ':thumbsup:',
    'up': ':rocket:',
    'undo': ':tada:',
    'unstaged': ':tada:',
    'added': ':tada:',
    'working-on': ':construction_worker:',
    'status': ':bar_chart:',
    'removed': ':tada:',
}


def display_list(action, items):
    if os_type == 'nt':
        import psutil
        shell_type = psutil.Process(os.getpid()).parent().parent().name()
        if shell_type == 'powershell.exe':
            print(colored(f'{EMOJI_ALIAS_UNICODE[icons[action]]} - {action}:', colors[action]))
        else:
            print(colored(f'* {action}:', colors[action]))

    else:
        print(colored(emoji.emojize(f'{icons[action]} - {action}:', use_aliases=True), colors[action]))
    for item in items:
        print(colored("  - " + item, colors[action]))


def display_list_no_icon(message, color, items):
    if os_type == 'nt':
        import psutil
        shell_type = psutil.Process(os.getpid()).parent().parent().name()
        if shell_type == 'powershell.exe':
            print(colored(f'{message}:', color))
        else:
            print(colored(f'* {message}:', color))

    else:
        print(colored(f'{message}:', color))
    for item in items:
        print(colored("  - " + item, color))


def display_message(message, color, icon):
    icon = f':{icon}:'
    if os_type == 'nt':
        import psutil
        shell_type = psutil.Process(os.getpid()).parent().parent().name()
        if shell_type == 'powershell.exe':
            print(colored(f'{EMOJI_ALIAS_UNICODE[icon]} - {message}', color))
        else:
            print(colored(f'* {message}', color))
    else:
        print(colored(emoji.emojize(f'{icon} - {message}', use_aliases=True), color))


def display_diff(diff):
    if diff.startswith('+++') or diff.startswith('---'):
        print(colored(diff, 'white'))
    elif diff.startswith('+'):
        print(colored(diff, 'green'))
    elif diff.startswith('-'):
        print(colored(diff, 'red'))
    else:
        print(colored(diff, 'white'))

if __name__ == '__main__':

    os_type = 'nt'

    display_message('some message', 'yellow', 'thumbsup')
    items = ['1', '2', '3', '4', '5']
    display_list('up', items)
