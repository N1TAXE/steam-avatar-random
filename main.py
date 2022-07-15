import requests
import os
import lxml
import yaml
from yaml import Loader
from bs4 import BeautifulSoup
from random import randrange

yaml_file = open('config.yaml', 'r')
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
    print(r.text)
    os.remove('ava.png')


if __name__ == '__main__':
    setAvatar()


