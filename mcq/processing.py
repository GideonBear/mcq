from pathlib import Path
from typing import List


def process(path: Path, process_type: str, process_value: str, whitelist: List[str], blacklist: List[str]):
    path = path.resolve()

    assert not (whitelist and blacklist)
    use_whitelist = bool(whitelist)
    lst = whitelist or blacklist
    whitelist = use_whitelist
    lst = list(map(lambda x: Path(x).resolve(), lst))

    assert process_type in process_type
    func = process_types[process_type]

    func(path, process_value, whitelist, lst)


def resize_div(path: Path, value: str, whitelist: bool, lst: List[str]):
    value = int(value)
    for p in path.iterdir():
        raise NotImplementedError


process_types = {
    'resize_div': resize_div,
    # todo
}
