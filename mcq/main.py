import contextlib
from argparse import ArgumentParser
from typing import Tuple

from .get import get, source_map as source_options


def main():
    source_type, source_value = parse_args()
    file = get(source_type, source_value)
    raise NotImplementedError


def parse_args() -> Tuple[str, str]:
    parser = ArgumentParser()

    parser.add_argument('source_type', options=source_options.keys())
    parser.add_argument('value')
    parser.add_argument('-d', '--resize-div', type=int)

    args = parser.parse_args()
    return args.source_type, source_options.get(args.value, args.value)
