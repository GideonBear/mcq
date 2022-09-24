import sys

from rich.console import Console as _Console

FATAL = 'bright_red'

console = _Console()


def fatal(msg):
    console.print(f'ERROR: {msg}', style=FATAL)
    sys.exit(1)


def set_verbose(val: bool):
    if val:
        global log
        log = _log


_log = console.print


def _dummy(msg): pass


log = _dummy
