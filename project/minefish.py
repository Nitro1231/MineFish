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
# Last Modified: Thursday, December 30, 2021 at 12:54 AM. (KST)
#
# This project is licensed under the GNU Affero General Public License v3.0;
# you may not use this file except in compliance with the License.


import cv2
import json
import imutils
import pyautogui
import pygetwindow
import numpy as np


SETTING_PATH = '.\\setting.json'
MATCHED_COLOR = (196, 229, 56)
MATCH_LIST = {
    'include': ['Minecraft', '.'],  # '.'
    'exclude': ['Launcher', 'Updater', 'MineFish']  # Launcher
}


class WindowTooSmallError(Exception):
    pass


class MineFish():
    def __init__(self) -> None:
        self.setting = None
        self.game_window = None
        self.load_setting()
        self.load_target_image()

    def load_setting(self) -> None:
        with open(SETTING_PATH, 'r', encoding='utf-8') as f:
            self.setting = json.load(f)

    def save_setting(self) -> None:
        with open(SETTING_PATH, 'w', encoding='utf-8') as f:
            json.dump(self.setting, f, indent='\t')

    def load_target_image(self) -> None:
        target_image_raw = cv2.imread(self.setting['image'])
        self.target_image = cv2.cvtColor(target_image_raw, cv2.COLOR_BGR2GRAY)

    def select_matched_window(self) -> None:
        self.game_window = None
        for window in pygetwindow.getAllWindows():
            if self._match_text(window.title, MATCH_LIST):
                self.game_window = window
                break

    def detect(self) -> tuple():
        left, top, width, height = self._get_window_size(self.game_window)
        p1, p2 = self._get_capture_points(left, top, width, height)

        org_image, gray_image = self._capture_area(p1, p2)
        return self._image_match(org_image, gray_image)

    def _match_text(self, text: str, match_list: dict()) -> bool:
        include = True
        exclude = True

        for word in match_list['include']:
            if not word in text:
                include = False
                break

        for word in match_list['exclude']:
            if word in text:
                exclude = False
                break

        return include and exclude

    def _get_window_size(self, handle: pygetwindow.Win32Window) -> tuple():
        left, top = handle.left, handle.top
        width, height = handle.width, handle.height
        return left, top, width, height

    def _get_capture_points(self, left: int, top: int, width: int, height: int) -> tuple(tuple()):
        p1 = (left + int(width / 2), top + int(height / 5 * 3))
        p2 = (int(width / 2), int(height / 5 * 2))
        return p1, p2

    def _capture_area(self, p1: tuple, p2: tuple) -> tuple():
        org_image = np.array(pyautogui.screenshot(region=p1+p2))
        gray_image = cv2.cvtColor(org_image, cv2.COLOR_BGR2GRAY)
        return org_image, gray_image

    def _image_match(self, org_image: np.ndarray, gray_image: np.ndarray) -> tuple():
        target_w, target_h = self.target_image.shape[::-1]
        image_w, image_h = gray_image.shape[::-1]
        min_w = target_w * self.setting['min_scale']
        min_h = target_h * self.setting['min_scale']

        if image_w < min_w or image_h < min_h:
            raise WindowTooSmallError()

        for scale in np.linspace(self.setting['min_scale'], self.setting['max_scale'], self.setting['frequency']):
            # Resizing
            target = imutils.resize(
                image=self.target_image,
                width=int(self.target_image.shape[1] * scale)
            )
            target_w, target_h = target.shape[::-1]

            try:
                res = cv2.matchTemplate(gray_image, target, cv2.TM_CCOEFF_NORMED)

                loc = np.where(res >= self.setting['accuracy'])
                if len(list(zip(*loc[::-1]))) > 0:
                    # Image detected.
                    for pt in zip(*loc[::-1]):
                        # Draw a rectangle on the detected area.
                        cv2.rectangle(
                            org_image, pt,
                            (pt[0] + target_w, pt[1] + target_h),
                            MATCHED_COLOR, 2
                        )
                        return True, org_image
            except:
                break
        return False, org_image
