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

import os
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

    def verify_setting(self) -> bool:
        self.check_file(self.setting, 'image')
        self.check_file(self.setting, 'display_language')
        self.check_value(self.setting, 'accuracy', 0.3, 0.9)
        self.check_value(self.setting, 'detection_delay', 0.1, 0.5)
        self.check_value(self.setting, 'throwing_delay', 0.3, 1.0)

    def check_file(self, setting: dict(), key: str):
        if key in setting:
            if not os.path.exists(setting[key]):
                raise FileNotFoundError
        else:
            raise NameError

    def check_value(self, setting: dict(), key: str, min_value: float, max_value: float):
        if key in setting:
            if not min_value <= setting[key] <= max_value:
                raise ValueError
        else:
            raise NameError

# TEST:
# s = Setting()
# s.setting['image'] = 'kr'
# s.save_setting(SETTING_PATH)
# print(s.setting)
