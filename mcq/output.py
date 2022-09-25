import sys

from rich.console import Console as _Console

FATAL = 'bright_red'

console = _Console()


def fatal(msg):
    console.print(f'ERROR: {msg}', style=FATAL)
    sys.exit(1)


verbose: bool = False


def set_verbose(val: bool):
    global verbose
    verbose = val


def log(msg):
    if verbose:
        console.print(msg)
