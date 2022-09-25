from argparse import ArgumentParser
from pathlib import Path

from .get import get, source_types
from .output import set_verbose
from .post_processing import post_process
from .processing import process_types, process


curr = Path('curr')

NORMAL_VALUE = 'assets/minecraft/textures/block,assets/minecraft/textures/item,assets/minecraft/textures/entity'


def main():
    args = parse_args()
    set_verbose(args.verbose)
    print('Collecting resource pack...')
    get(args.source_type, args.source_value, curr)
    print('Collected resource pack')
    print('Processing resource pack...')
    process(curr, args.process_type, args.process_value, args.whitelist or [], args.blacklist or [])
    print('Processed resource pack')
    print('Post-processing resource pack...')
    post_process(curr, args.export_only_textures, args.zip)
    print('Done')


def parse_args():
    parser = ArgumentParser()

    parser.add_argument('source_type', choices=source_types.keys(), help='Where to get the resource pack from')
    parser.add_argument('source_value', help='The url, path, version, etc')

    parser.add_argument('process_type', choices=process_types.keys(), help='What to do with the resource pack')
    parser.add_argument('process_value', type=int, default=None, help='How much to do that')
    lists = parser.add_mutually_exclusive_group()
    lists.add_argument('-b', '--blacklist', type=parse_list, help='Exclude files and folders from the process')
    lists.add_argument('-w', '--whitelist', type=parse_list, help='Only perform the process on these folders')
    lists.add_argument(
        '-n', '--normal',
        action='store_const',
        dest='whitelist', const=NORMAL_VALUE,
        help=f'Only preform the process on the "normal" folders, use the whitelist {NORMAL_VALUE}'
    )

    parser.add_argument(
        '-t', '--export-only-textures',
        action='store_true',
        help='Delete everything but "assets/minecraft/textures", "pack.mcmeta" and "pack.png"'
    )
    parser.add_argument('-z', '--zip', action='store_true', help='Zip after processing')

    parser.add_argument('-v', '--verbose', action='store_true', help='Put more useless stuff on the screen')

    return parser.parse_args()


def parse_list(s: str):
    return [int(item) for item in s.split(',')]
