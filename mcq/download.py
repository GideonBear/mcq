import shutil
from base64 import urlsafe_b64decode, urlsafe_b64encode
from pathlib import Path

from .output import fatal


cache = Path('cache')
if cache.is_file():
    fatal(f'Did not expect {cache} to be a file')
cache.mkdir(exist_ok=True)


def encode(data: str) -> str:
    return str(urlsafe_b64encode(data.encode()))


def decode(data: str) -> str:
    return str(urlsafe_b64decode(data))


def download(url: str, dest: Path):
    file = cache / encode(url)
    if file.exists():
        shutil.copy(file, dest)
        return


    raise NotImplementedError
