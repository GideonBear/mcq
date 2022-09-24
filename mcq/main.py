from argparse import ArgumentParser
from pathlib import Path

from .get import get, source_types
from .post_processing import post_process
from .processing import process_types, process

curr = Path('curr')


def main():
    args = parse_args()
    print(args)
    get(args.source_type, args.source_value, curr)
    process(curr, args.process_type, args.process_value)
    post_process(curr, args.only_textures)
    raise NotImplementedError


def parse_args():
    parser = ArgumentParser()

    parser.add_argument('source_type', choices=source_types.keys())
    parser.add_argument('source_value')
    parser.add_argument('process_type', choices=process_types.keys())
    parser.add_argument('process_value')
    parser.add_argument('--only-textures', action='store_true')
    # todo: --zip and --no-zip (zip being the default)

    return parser.parse_args()
