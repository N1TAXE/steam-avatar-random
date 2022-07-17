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
        'version': sys.argv[1]
    }
    yaml.dump(data, f)


os.system(f'pyinstaller -F --onefile --icon=ico.ico --name "SRA_{sys.argv[1]}" main.py')

with zipfile.ZipFile('dist/update.zip', 'w') as update:
    update.write(f'dist/SRA_{sys.argv[1]}.exe', basename(f'dist/SRA_{sys.argv[1]}.exe'))

os.system(f'git commit -m "update v{sys.argv[1]}" dist/update.zip version.yml')
os.system('git push')