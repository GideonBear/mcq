from os import PathLike
from pathlib import Path
from typing import List, Optional, Tuple

from PIL import Image

from .output import log, fatal, debug
from .pathlist import create_pathlist


def process(
        path: Path,
        process_type: str,
        process_value: Optional[int],
        whitelist: List[PathLike],
        blacklist: List[PathLike]
):
    path = path.resolve()

    whitelist, lst = create_pathlist(whitelist, blacklist)

    assert process_type in process_type
    func, need_value, do_dirs = process_types[process_type]
    if need_value and process_value is None:
        fatal('A process_value is needed for this process')
    elif (not need_value) and process_value is not None:
        fatal('Specified process_value is not accepted for this process')

    process_rec(path, func, process_value, whitelist, lst, do_dirs)


def get_lst(path: Path, whitelist: List[PathLike], blacklist: List[PathLike]) -> Tuple[bool, List[Path]]:

    if use_whitelist:
        [lst.extend(p.parents[:-1]) for p in lst.copy()]

    lst = list(map(lambda x: (path / x).resolve(), lst))

    debug(lst)
    return use_whitelist, lst


def process_rec(path: Path, func, value: int, whitelist: bool, lst: List[Path], do_dirs: bool):
    for p in path.iterdir():
        if skip(p, whitelist, lst):
            log(f'Skipping {p}')
        elif p.is_dir():
            process_rec(p, func, value, whitelist, lst, do_dirs=do_dirs)
            if do_dirs:
                func(p, value)
        else:
            func(p, value)


def skip(path: Path, whitelist: bool, lst: List[Path]):
    assert path == path.resolve()
    debug(f'`skip` called with {whitelist=}, {path=}')

    if whitelist:
        for p in path.parents:
            if p in lst:
                return False
        return True


def resize_div(path: Path, value: int):
    if path.suffix != '.png':
        return
    with Image.open(str(path)) as image:
        width, height = map(div_helper(value), (image.width, image.height))
        image = image.resize((width, height))
        image.save(path)


def div_helper(value):
    def div_helper_closure(old):
        new = old // value
        return 1 if new == 0 else new

    return div_helper_closure


def delete(path: Path, _: int):
    if path.is_dir():
        try:
            path.rmdir()
        except OSError:
            # Not empty, insides were skipped
            pass
    else:
        path.unlink()


process_types = {
    'resize_div': (resize_div, True, False),
    'delete': (delete, False, True)
}
