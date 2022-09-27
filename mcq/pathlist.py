from abc import ABC, abstractmethod
from os import PathLike
from pathlib import Path
from typing import List


def create_pathlist(whitelist: List[PathLike], blacklist: List[PathLike]):
    whitelist = list(map(Path, whitelist))
    blacklist = list(map(Path, blacklist))
    if whitelist and blacklist:
        raise ValueError('Either whitelist or blacklist can contain entries')
    use_whitelist = bool(whitelist)
    lst = whitelist or blacklist
    if use_whitelist:
        return PathWhitelist(lst)
    else:
        PathBlacklist(lst)


class PathList(ABC):
    def __init__(self, lst: List[Path]):
        self.list = lst

    @abstractmethod
    def skip(self, path: Path, extra_value: bool) -> bool:
        ...


class PathWhitelist(PathList):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        [self.list.extend(p.parents[:-1]) for p in self.list.copy()]

    def skip(self, path: Path, whitelisted: bool) -> bool:
        if path.is_dir():
            return path not in self.list
        else:
            return whitelisted


class PathBlacklist(PathList):
    def skip(self, path: Path, _: bool) -> bool:
        return path in self.list
