# config.py
#
# Copyright 2020 Nitro. All Rights Reserved.
#
# Developer: Nitro (admin@nitrostudio.dev)
# Blog: https://blog.nitrostudio.dev
# Discord: Nitro#1781
# GitHub: https://github.com/Nitro1231/MineFish
#
# Version: 4.0.0
# Last Modified: Monday, December 6, 2021 at 11:11 AM. (PDT)
#
# This project is licensed under the GNU Affero General Public License v3.0;
# you may not use this file except in compliance with the License.

import json


class Setting():
    def __init__(self, setting_path) -> None:
        self.setting_path = setting_path
        self.setting = self.load_setting(setting_path)

    def load_setting(self, path: str) -> None:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_setting(self, path: str) -> None:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.setting, f, indent='\t')

# TEST:
# s = Setting()
# s.setting['image'] = 'kr'
# s.save_setting(SETTING_PATH)
# print(s.setting)
