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
import time
import setting
import image_detection
import window_manager

SETTING_PATH = './setting.json'
FREQUENCY = 20
MIN_SCALE = 0.5
MAX_SCALE = 1.5
MATCH = {
    'include': ['Minecraft'],
    'exclude': ['Launcher']
}

class MineFish():
    def __init__(self) -> None:
        self.setting = setting.Setting(SETTING_PATH)
        self.verify_setting()

        self.image_detection = image_detection.ImageDetection(
            target_path = self.setting['image'],
            accuracy = self.setting['accuracy'],
            frequency = FREQUENCY,
            min_scale = MIN_SCALE,
            max_scale = MAX_SCALE
        )

        self.window = None

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

    def capture_window(self) -> 'Win32Window':
        while True:
            window = window_manager.get_matched_window(MATCH)
            print(window)
            if window != None:
                return window
            time.sleep(0.5)

    def detect():
        pass

    def get_capture_points(self, x: int, y: int, width: int, height: int) -> tuple(tuple()):
        p1 = (x + int(width/2), y + int(height/3))
        p2 = (int(width/2), int(height/3*2))


MineFish()

# window = window_manager.get_matched_window(MATCH)
# while True:
#     print(window_manager.get_window_size(window))
#     time.sleep(0.5)