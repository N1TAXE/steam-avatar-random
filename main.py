import requests
import os
import lxml
import yaml
import sys
from yaml import Loader
from bs4 import BeautifulSoup
from random import randrange

ruLink = 'https://rustic-salad-7e9.notion.site/SteamID64-SteamLoginSecure-64efe3b1b363406d81ccb59acec6a2f3'
engLink = 'https://rustic-salad-7e9.notion.site/SteamID64-SteamLoginSecure-64efe3b1b363406d81ccb59acec6a2f3'

if not os.path.exists('lang.yml'):
    print('Choose language / Выберите язык\n(ru/eng):')
    lang = input()
    configData = {
        'language': lang.lower(),
    }
    with open('lang.yml', 'w') as f:
        yaml.dump(configData, f)

yaml_file = open('lang.yml', 'r')
lang = yaml.load(yaml_file, Loader=Loader)['language']

if lang == 'ru':
    _sidEnter = 'Введите SteamID64:'
    _slsEnter = f'Введите Steam Login Secure:\n(Где найти: {ruLink})'
elif lang == 'eng':
    _sidEnter = 'Enter SteamID64:'
    _slsEnter = f'Enter Steam Login Secure:\n(How to get: {engLink})'

if not os.path.exists('config.yml'):
    print(_sidEnter)
    sid = input()
    print(_slsEnter)
    sls = input()
    configData = {
        'steamid': int(sid),
        'steamloginsecure': sls
    }
    with open('config.yml', 'w') as f:
        yaml.dump(configData, f)


yaml_file = open('config.yml', 'r')
config = yaml.load(yaml_file, Loader=Loader)


url = 'https://steamcommunity.com/actions/FileUploader'
avatars = 'https://randomavatar.com/'
id = config['steamid']

def getCookies():
    session = requests.Session()
    session.get('http://steamcommunity.com/login/oxxyon')
    return session.cookies.get_dict()['sessionid']

cook = getCookies()

cookies = {
    'steamLoginSecure': config['steamloginsecure'],
    'sessionid': cook,
}
data = {
    "MAX_FILE_SIZE": "1048576",
    "type": "player_avatar_image",
    "sId": id,
    "sessionid": cook,
    "doSub": "1",
}
avas = []


def getAvatar():
    r = requests.post(url=avatars)
    soup = BeautifulSoup(r.text, "lxml")
    ava = soup.find_all("div", class_="col-sm-2 col-xs-3")
    for i in ava:
        i = i.find("img").get("src")
        avas.append(i)
    image = requests.get(avas[randrange(len(avas))]).content
    filename = 'ava.png'
    with open(filename, "wb") as f:
        f.write(image)
    picture = open('ava.png', 'rb')

    return picture


def setAvatar():
    r = requests.post(url=url, params={'type': 'player_avatar_image', 'sId': id}, files={'avatar': getAvatar()}, data=data,
                  cookies=cookies)
    if "You've made too many requests recently" in r.text:
        if lang == 'ru':
            print('Аватарка не изменена, слишком много запросов, подождите немного и попробуйте еще раз!')
            input('Нажмите Enter для выхода')
        elif lang == 'eng':
            print('Avatar not changed, too many requests, please wait and try again later!')
            input('Press Enter to exit')
    else:
        print("DONE!")
    os.remove('ava.png')


if __name__ == '__main__':
    setAvatar()


