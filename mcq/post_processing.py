from pathlib import Path
from shutil import make_archive, rmtree

from .processing import process

TEXTURES_PATH = 'assets/minecraft/textures'


def post_process(path: Path, export_only_textures: bool, zip_: bool):
    if export_only_textures:
        do_export_only_textures(path)
    if zip_:
        do_zip(path)


def do_export_only_textures(path: Path):
    print('Deleting with blacklist...')
    process(path, 'delete', None, [], [TEXTURES_PATH, 'pack.mcmeta', 'pack.png'])


def do_zip(path: Path):
    result = make_archive(path.name, 'zip', path, path)
    assert result == f'{path}.zip'
    rmtree(path)
