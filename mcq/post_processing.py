from pathlib import Path


def post_process(dir: Path, only_textures: bool):
    if only_textures:
        do_only_textures()


def do_only_textures():
    raise NotImplementedError
