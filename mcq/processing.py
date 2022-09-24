from pathlib import Path
from typing import List, Tuple

from PIL import Image

from .output import log


def process(path: Path, process_type: str, process_value: str, whitelist: List[str], blacklist: List[str]):
    path = path.resolve()

    assert not (whitelist and blacklist)
    use_whitelist = bool(whitelist)
    lst = whitelist or blacklist
    whitelist = use_whitelist
    lst = list(map(lambda x: Path(x).resolve(), lst))

    assert process_type in process_type
    func = process_types[process_type]

    func(path, int(process_value), whitelist, lst)


def resize_div(path: Path, value: int, whitelist: bool, lst: List[str]):
    for p in path.iterdir():
        if (whitelist and p not in lst) or (p in lst):
            log(f'Skipping {p}')
        elif p.is_dir():
            resize_div(path, value, whitelist, lst)
        else:
            resize_div_one(p, value)


def resize_div_one(path: Path, value: int):
    with Image.open(str(path)) as image:
        width, height = map(div_helper(value), (image.width, image.height))
        image = image.resize((width, height))
        image.save(path)


def div_helper(value):
    def div_helper_closure(old):
        new = old // 2
        return 1 if new == 0 else new
    return div_helper_closure


process_types = {
    'resize_div': resize_div
}
