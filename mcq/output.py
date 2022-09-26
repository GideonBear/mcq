import sys
from pprint import pprint

from rich.console import Console as _Console

FATAL = 'bright_red'

console = _Console()


def fatal(msg):
    console.print(f'ERROR: {msg}', style=FATAL)
    sys.exit(1)


verbose: bool = False
debug_val: bool = False


def set_verbose(val: bool):
    global verbose
    verbose = val


def set_debug(val: bool):
    global debug_val
    debug_val = val


def log(msg):
    if verbose:
        console.print(msg)


def debug(msg):
    if debug_val:
        pprint(msg)
