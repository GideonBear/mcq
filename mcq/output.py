import sys
from pprint import pprint
from typing import Any, Union

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
        print(msg)


def debug(val_msg: Union[str, Any] = 'temporary debug message', val: Any = None):
    if debug_val:
        if val:
            print(val_msg, end='')
            pprint(val)
        elif isinstance(val_msg, str):
            print(val_msg)
        else:
            pprint(val_msg)
