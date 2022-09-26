import shutil
from shutil import copytree, unpack_archive
from pathlib import Path

from .default import default_urls
from .download import download
from .output import fatal


ZIP_SUFFIX = '.zip'


def remove_prefix(text: str, prefix: str) -> str:
    if text.startswith(prefix):
        return text[len(prefix):]
    return text


def compare_version(version: str) -> float:
    return float(remove_prefix(version, '1.'))


def get(source_type, source_value, dest: Path):
    if dest.exists():
        fatal(f'"{dest}" exists, remove or move it before running')

    assert source_type in source_types
    func = source_types[source_type]

    func(source_value, dest)


def from_default(version: str, dest: Path):
    if version not in default_urls:
        versions = '\n'.join(sorted(default_urls.keys(), key=compare_version, reverse=True))
        fatal(f'Unsupported version, available versions are:\n\n{versions}')

    url = default_urls[version]
    from_url(url, dest)


def from_url(url: str, dest: Path):
    with download(url) as file:
        from_zip(file, dest)


def from_dir(path, dest: Path):
    directory = Path(path).resolve()
    if not directory.is_dir():
        fatal(f'Path "{path}" does not exist or is not a directory')
    print('Copying...')
    copytree(directory, dest)


def from_zip(path, dest: Path):
    zip_file = Path(path).resolve()
    if not zip_file.is_file():
        fatal(f'Path "{path}" does not exist or is a directory')
    try:
        print('Unpacking...')
        unpack_archive(path, dest)
    except shutil.ReadError as err:
        fatal(f'Error while unpacking archive: {err}')


source_types = {
    'default': from_default,
    'url': from_url,
    'dir': from_dir,
    'zip': from_zip
}
