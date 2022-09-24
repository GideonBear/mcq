from pathlib import Path


TEXTURES_PATH = 'assets/minecraft/textures'


def post_process(path: Path, only_textures: bool):
    if only_textures:
        do_only_textures(path)


def do_only_textures(path: Path):
    textures = path / TEXTURES_PATH
    raise NotImplementedError
