import requests


VERSION = '4.0.0'
URL = 'https://nitro1231.github.io/Database/Update/V0/MineFish/Update.json'


def check_update():
    req = requests.get(URL)
    if req.status_code == 200:
        return True, req.json()
    else:
        return False, None
