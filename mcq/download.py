from base64 import urlsafe_b64decode, urlsafe_b64encode
from contextlib import contextmanager
from pathlib import Path

from .output import fatal, log

cache = Path('cache')
if cache.is_file():
    fatal(f'Did not expect {cache} to be a file')
cache.mkdir(exist_ok=True)


def encode(data: str) -> str:
    return str(urlsafe_b64encode(data.encode()))


@contextmanager
def download(url: str) -> Path:
    file = cache / encode(url)
    if not file.exists():
        print('File not cached, downloading...')
        log(f'File: {file.name}')
        _download(url, file)
    yield file
    # don't delete it as it's in the cache, not a temporary file


def _download(url, dest):
    raise NotImplementedError
