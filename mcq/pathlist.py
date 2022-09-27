from abc import ABC, abstractmethod
from os import PathLike
from pathlib import Path
from typing import List

from .output import debug


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
        return PathBlacklist(lst)


class PathList(ABC):
    def __init__(self, lst: List[Path]):
        self.list = lst
        debug(f'{self.__class__.__name__}:\n', self.list)

    @abstractmethod
    def skip(self, path: Path, extra_value: bool, extra_value_2: bool) -> bool:
        ...


class PathWhitelist(PathList):
    def __init__(self, lst: List[Path]):
        [lst.extend(list(p.parents)[:-1]) for p in lst.copy()]
        super().__init__(lst)

    def skip(self, path: Path, whitelisted: bool, is_dir: bool) -> bool:
        if is_dir:
            return path not in self.list
        else:
            return not whitelisted


class PathBlacklist(PathList):
    def skip(self, path: Path, _: bool, __: bool) -> bool:
        return path in self.list
