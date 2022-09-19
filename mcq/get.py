from pathlib import Path


curr = Path('curr')  # make better


def get(source_type, value) -> Path:
    func = source_map[source_type]
    func(value)

    return curr


def default(version):
    pass


def url(url):
    pass


def file(path):
    path = Path(path).resolve()


source_map = {
    'default': default,
    'url': url,
    'file': file
}
