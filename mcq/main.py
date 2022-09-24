from argparse import ArgumentParser
from pathlib import Path

from .get import get, source_types
from .output import set_verbose
from .post_processing import post_process
from .processing import process_types, process

curr = Path('curr')


def main():
    args = parse_args()
    set_verbose(args.verbose)
    print('Collecting resource...')
    get(args.source_type, args.source_value, curr)
    print('Collected resource')
    print('Processing resource...')
    process(curr, args.process_type, args.process_value, args.whitelist, args.blacklist)
    print('Processed resource')
    print('Post-processed resource')
    post_process(curr, args.only_textures, args.zip)
    print('Done')


def parse_args():
    parser = ArgumentParser()

    # todo: add argument help
    parser.add_argument('source_type', choices=source_types.keys())
    parser.add_argument('source_value')
    parser.add_argument('process_type', choices=process_types.keys())
    parser.add_argument('process_value')
    parser.add_argument('-t', '--only-textures', action='store_true')
    parser.add_argument('-z', '--zip', action='store_true')
    lists = parser.add_mutually_exclusive_group()
    lists.add_argument('-b', '--blacklist', type=parse_list)
    lists.add_argument('-w', '--whitelist', type=parse_list)
    parser.add_argument('-v', '--verbose', action='store_true')

    return parser.parse_args()


def parse_list(s: str):
    return [int(item) for item in s.split(',')]
