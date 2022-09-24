from pathlib import Path
from shutil import copytree

from .default import default_urls
from .output import fatal

curr = Path('curr')  # make better


def get(source_type, value) -> Path:
    assert source_type in source_map
    func = source_map[source_type]
    func(value)

    return curr


def from_default(version: str):
    version = version.removeprefix('1.')
    if version not in default_urls:
        fatal('Unsupported version, available versions are:\n\n' + '\n'.join(default_urls.keys()))
    raise NotImplementedError


def from_url(url: str):
    raise NotImplementedError


def from_dir(path):
    directory = Path(path).resolve()
    if not directory.is_dir():
        fatal(f'Path {path} does not exist or is not a directory')
    copytree(directory, curr)
    raise NotImplementedError


def from_zip(path):
    zip_file = Path(path).resolve()
    if not zip_file.is_file():
        fatal(f'Path {path} does not exist or is a directory')
    raise NotImplementedError


source_map = {
    'default': from_default,
    'url': from_url,
    'dir': from_dir,
    'zip': from_zip
}
