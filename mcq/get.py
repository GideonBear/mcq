from pathlib import Path


curr = Path('curr')  # make better


def get(source_type, value) -> Path:
    func = source_map[source_type]
    func(value)

    return curr


curseforge_vanilladefault_url = 'https://www.curseforge.com/minecraft/texture-packs/vanilladefault/download/{}/file'
curseforge_vanilladefault = {

}
texturepackscom_url = 'https://texture-packs.com/default-texture-pack-1-{}-download/'
texturepackscom_supported = '17 16 15 14 13 12 10 8'.split(' ')
texturepackscom_other = {
    '11': '12',
    '9': '10'
}


def from_default(version: str):
    version = version.removeprefix('1.')
    raise NotImplementedError


def from_url(url: str):
    raise NotImplementedError


def from_file(path):
    path = Path(path).resolve()
    if not path.exists():
        raise NotImplementedError
    raise NotImplementedError


source_map = {
    'default': from_default,
    'url': from_url,
    'file': from_file
}
