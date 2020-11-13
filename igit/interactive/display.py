from rich.console import Console


class Display:

    def __init__(self,) -> None:
        self.console = Console()

    def message(self, text, color='white', icon='poop'):
        self.console.print(f':{icon}: - {text}', style=f'bold {color}')

    def list(self, text, items, color, icon):
        self.console.print(f':{icon}: - {text}', style=f'bold {color}')
        for item in items:
            self.console.print(" " * 8 + item, style='white')

    def diff(self, diff):
        if diff.startswith('+++') or diff.startswith('---'):
            self.console.print(diff, style=f'bold white')
        elif diff.startswith('+'):
            self.console.print(diff, style=f'bold green')
        elif diff.startswith('-'):
            self.console.print(diff, style=f'bold red')
        else:
            self.console.print(diff, style=f'white')


if __name__ == '__main__':

    display = Display()
    display.message('hello', 'green', 'thumbsup')
    display.list('hello', ['item1', 'item2'], 'green', 'thumbsup')

