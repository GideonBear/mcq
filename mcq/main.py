from argparse import ArgumentParser
from pathlib import Path

from .get import get, source_map as source_options


curr = Path('curr')


def main():
    args = parse_args()
    file = get(args.source_type, args.source_value, curr)
    raise NotImplementedError


def parse_args():
    parser = ArgumentParser()

    parser.add_argument('source_type', choices=source_options.keys())
    parser.add_argument('source_value')
    parser.add_argument('-d', '--resize-div', type=int)

    return parser.parse_args()
