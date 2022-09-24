def get_urls(versions, url):
    return {k: url.format(v) for k, v in versions.items()}


vd_url = 'https://www.curseforge.com/minecraft/texture-packs/vanilladefault/download/{}/file'
vd_files = {
    #  todo
}
vd_urls = get_urls(vd_files, vd_url)

t_url = 'https://texture-packs.com/default-texture-pack-1-{}-download/'
t_supported = '17 16 15 14 13 12 10 8'.split(' ')
t_other = {
    '11': '12',
    '9': '10'
}
t_versions = dict(zip(t_supported, t_supported))
t_versions.update(t_other)
t_urls = get_urls(t_versions, t_url)

default_urls = {**t_urls, **vd_urls}
