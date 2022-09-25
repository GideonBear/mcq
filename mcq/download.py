import contextlib
import shutil
from base64 import urlsafe_b64encode
from contextlib import contextmanager
from functools import partial
from pathlib import Path
from urllib.request import urlopen

from rich.progress import TimeRemainingColumn, TextColumn, TransferSpeedColumn, DownloadColumn, BarColumn, Progress

from .output import fatal, log

PROGRESS_REFRESH_PER_SECOND = 30

cache = Path('cache')
if cache.is_file():
    fatal(f'Did not expect {cache} to be a file')
cache.mkdir(exist_ok=True)

columns = (
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    DownloadColumn(),
    TransferSpeedColumn(),
    TextColumn("eta"),
    TimeRemainingColumn(),
)
progress = Progress(*columns, refresh_per_second=PROGRESS_REFRESH_PER_SECOND)


def encode(data: str) -> str:
    return str(urlsafe_b64encode(data.encode()))


@contextmanager
def download(url: str) -> Path:
    file = cache / encode(url)
    if not file.exists():
        print('File not cached, downloading...')
        log(f'File: {file.name}')
        unfinished = f'UNFINISHED-{file}'
        _download(url, unfinished)
        shutil.move(unfinished, file)
    yield file
    # don't delete it as it's in the cache, not a temporary file


def _download(url, dest):
    task_id = progress.add_task("download", filename=dest, start=False)
    with contextlib.closing(urlopen(url)) as response:
        # This will break if the response doesn't contain content length
        progress.update(task_id, total=int(response.info()["Content-length"]))
        with open(dest, "wb") as dest_file:
            progress.start_task(task_id)
            for data in iter(partial(response.read, 32768), b""):
                dest_file.write(data)
                progress.update(task_id, advance=len(data))

