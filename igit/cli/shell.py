from subprocess import PIPE, Popen
from termcolor import colored


def debug(mode):
    def wrapper(g):
        def full_debug(*args, **kwargs):
            debug_sep = '**************************'
            print(colored(f'running: {args[0]}', 'magenta'))
            rv = g(*args, **kwargs)
            print(colored('done.', 'magenta'))
            print(colored(debug_sep, 'blue'))
            return rv

        def pretty_debug(*args, **kwargs):
            debug_sep = '-------------------------'
            rv = g(*args, **kwargs)
            print(colored(debug_sep, 'blue'))
            return rv

        def no_debug(*args, **kwargs):
            return g(*args, **kwargs)

        if mode == 'full':
            return full_debug
        elif mode == 'pretty':
            return pretty_debug
        elif mode is None:
            return no_debug
    return wrapper


def shell(f):
    def wrapper(*args, **kwargs):
        std_output, std_error, return_code = f(*args, **kwargs)
        error = std_error.decode().strip() if std_error else None
        output = std_output.decode().strip() if std_output else None
        if return_code != 0 and error is not None:
            print(colored(error, 'red'))
            return None, error, return_code
        else:
            for message in (error, output):
                if message not in ['', None]:
                    print(message)
            return output, None, return_code
    return wrapper


@debug(None)
@shell
def run_cmd(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE):
    p = Popen(cmd, shell=True, stdout=stdout, stdin=stdin, stderr=stderr)
    output, err = p.communicate()
    return output, err, p.returncode
