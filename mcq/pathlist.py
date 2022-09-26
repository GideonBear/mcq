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


class _PathList(ABC):
    def __init__(self, lst: List[Path]):
        self.list = lst

    @abstractmethod
    def skip(self, path: Path) -> bool:
        ...


class PathWhitelist(_PathList):
    def skip(self, path: Path) -> bool:
        if path in self.list:
            return False


class PathBlacklist(_PathList):
    def skip(self, path: Path) -> bool:
        return path in self.list
