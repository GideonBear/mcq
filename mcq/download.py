import contextlib
import shutil
from base64 import urlsafe_b64encode
from contextlib import contextmanager
from functools import partial
from pathlib import Path
from urllib.request import urlopen, build_opener, install_opener

from rich.progress import TimeRemainingColumn, TextColumn, TransferSpeedColumn, DownloadColumn, BarColumn, Progress

from .output import fatal, log, console

PROGRESS_REFRESH_PER_SECOND = 30

cache = Path('cache')
if cache.is_file():
    fatal(f'Did not expect {cache} to be a file')
cache.mkdir(exist_ok=True)

columns = (
    TextColumn("[bold blue]{task.fields[file]}", justify="right"),
    BarColumn(),
    DownloadColumn(),
    TransferSpeedColumn(),
    TextColumn("eta"),
    TimeRemainingColumn(),
)
progress = Progress(*columns, console=console, refresh_per_second=PROGRESS_REFRESH_PER_SECOND)

opener = build_opener()
opener.addheaders = [('User-Agent',
                      (
                          'Mozilla/5.0 (Windows NT 6.1; WOW64)'
                          'AppleWebKit/537.36 (KHTML, like Gecko)'
                          'Chrome/36.0.1941.0 Safari/537.36'
                      ))]
install_opener(opener)


def encode(data: str) -> str:
    return urlsafe_b64encode(data.encode()).decode()


@contextmanager
def download(url: str) -> Path:
    file = cache / encode(url)
    file = file.with_suffix('.zip')
    if not file.exists():
        print('File not cached, downloading...')
        unfinished = file.with_name(f'UNFINISHED-{file.name}')
        _download(url, unfinished)
        shutil.move(unfinished, file)
    else:
        print('File cached')
    yield file
    # don't delete it as it's in the cache, not a temporary file


def _download(url, dest):
    log(f'Downloading {url} to {dest}')
    task_id = progress.add_task("download", file=url.split('/')[-1], start=False)
    with contextlib.closing(urlopen(url)) as response, progress:
        # This will break if the response doesn't contain content length
        total = int(response.info()["Content-length"])
        progress.update(task_id, total=total)
        with open(dest, "wb") as dest_file:
            progress.start_task(task_id)
            for data in iter(partial(response.read, 32768), b""):
                dest_file.write(data)
                progress.update(task_id, advance=len(data))
