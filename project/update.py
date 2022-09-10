# update.py
#
# Copyright 2020 Nitro. All Rights Reserved.
#
# Developer: Nitro (admin@nitrostudio.dev)
# Blog: https://blog.nitrostudio.dev
# Discord: Nitro#1781
# GitHub: https://github.com/Nitro1231/MineFish
#
# Version: 4.0.0
# Last Modified: Saturday, September 10, 2022, at 7:23 PM. (KST)
#
# This project is licensed under the GNU Affero General Public License v3.0;
# you may not use this file except in compliance with the License.


import requests


URL = 'https://nitro1231.github.io/Database/Update/V0/MineFish/Update.json'


def check_update():
    req = requests.get(URL)
    if req.status_code == 200:
        return True, req.json()
    else:
        return False, None
