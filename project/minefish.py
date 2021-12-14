# minefish.py
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
import setting
import image_detection
import window_manager

SETTING_PATH = './setting.json'
MIN_SCALE = 0.5
MAX_SCALE = 1.5


class MineFish():
    def __init__(self) -> None:
        self.setting = setting.Setting(SETTING_PATH)
        self.verify_setting()

    def verify_setting(self) -> bool:
        setting = self.setting.setting
        self.check_file(setting, 'image')
        self.check_file(setting, 'display_language')
        self.check_value(setting, 'accuracy', 0.3, 0.9)
        self.check_value(setting, 'detection_delay', 0.1, 0.5)
        self.check_value(setting, 'throwing_delay', 0.3, 1.0)

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

    def get_capture_points(x, y, width, height) -> tuple(tuple()):
        p1 = (x + int(width/2), y + int(height/3))
        p2 = (int(width/2), int(height/3*2))

    def detect():
        pass


MineFish()
