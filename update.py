import os
import requests
import yaml
import sys
import zipfile
from yaml import Loader
from os.path import basename

newversion = sys.argv

with open('version.yml', 'w') as f:
    data = {
        'varsion': sys.argv[1]
    }
    yaml.dump(data, f)

def getVersion():
    r = requests.get('https://raw.githubusercontent.com/N1TAXE/steam-avatar-random/master/version.yml')
    return yaml.load(r.text, Loader=Loader)['version']

os.system(f'pyinstaller -F --onefile --icon=ico.ico --name "SRA_{getVersion()}" main.py')

with zipfile.ZipFile('dist/update.zip', 'w') as update:
    update.write(f'dist/SRA_{getVersion()}.exe', basename(f'dist/SRA_{getVersion()}.exe'))