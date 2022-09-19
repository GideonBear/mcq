from argparse import ArgumentParser
from typing import Tuple

from .get import get


def main():
    file = get(*parse_args())
    raise NotImplementedError


def parse_args() -> Tuple[str, str]:
    parser = ArgumentParser()

    source_options = {
        'd': 'default',
        'u': 'url',
        'f': 'file'
    }
    source_options_list = tuple(source_options.keys()) + tuple(source_options.values())

    parser.add_argument('source_type', options=source_options_list)
    parser.add_argument('value')

    args = parser.parse_args()
    return args.source_type, source_options.get(args.value, args.value)
