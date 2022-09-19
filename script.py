from pathlib import Path
from shutil import copytree, rmtree, make_archive
from PIL import Image

PATH = '/home/gideonbeerens/mcq/'

vaste_resolutie = input('Vaste resolutie? (y/n) > ') == 'y'
resolutie = int(input('Resolutie > '  if vaste_resolutie else 'Resolutie delen door > '))

dest = PATH+f'newpacks/{"vast" if vaste_resolutie else "deeldoor"}{resolutie}'
try:
	rmtree(dest)
	print('Deleted already existing pack')
except FileNotFoundError:
	pass
copytree(PATH+'pack', dest)
print(f'Copied pack to newpack, destination {dest}')

for path in Path(dest).rglob('*.png'):
	path = str(path)
	image = Image.open(path)
	if vaste_resolutie:
		image = image.resize((resolutie, resolutie), Image.ANTIALIAS)
	else:
		x, y = image.size
		if x < resolutie or y < resolutie:
			print(f'Skipping {path}')
			continue
		image = image.resize((int(x/resolutie), int(y/resolutie)), Image.ANTIALIAS)
	image.save(path)
print('Written cropped files')


with open(dest+'/pack.mcmeta', 'w') as f:
	f.write('''
{
  "pack": {
    "pack_format": 8,
    "description": "Gideon\'s cursed pack"
}
''')
print('Written pack.mcmeta')

make_archive(dest, 'zip', dest)
print(f'Zipped folder to {dest+".zip"}')

print('Done')