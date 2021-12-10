# image_detection.py
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


import cv2
import numpy as np
import pyautogui
import imutils


class ImageDetection():
    def __init__(self, target_path: str, accuracy: float, min_scale: float, max_scale: float) -> None:
        target_image = cv2.imread(target_path)
        self._target = cv2.cvtColor(target_image, cv2.COLOR_BGR2GRAY)
        self._accuracy = accuracy
        self._min_scale = min_scale
        self._max_scale = max_scale

    def capture_area(self, p1: tuple, p2: tuple) -> tuple():
        org_image = np.array(pyautogui.screenshot(region=p1+p2))
        gray_image = cv2.cvtColor(org_image, cv2.COLOR_BGR2GRAY)
        return org_image, gray_image

    def image_match(self, org_image: np.ndarray, gray_image: np.ndarray) -> tuple():
        target_w, target_h = self._target.shape[::-1]
        image_w, image_h = gray_image.shape[::-1]
        min_w = target_w * self._min_scale
        min_h = target_h * self._min_scale

        if image_w < min_w or image_h < min_h:
            raise ValueError

        for scale in np.linspace(self._min_scale, self._max_scale, 30)[::-1]:
            # Resizing
            target = imutils.resize(
                image=self._target,
                width=int(self._target.shape[1] * scale)
            )
            target_w, target_h = target.shape[::-1]

            res = cv2.matchTemplate(gray_image, target, cv2.TM_CCOEFF_NORMED)

            loc = np.where(res >= self._accuracy)
            if len(list(zip(*loc[::-1]))) > 0:
                # Image detected.
                for pt in zip(*loc[::-1]):
                    # Draw a rectangle on the detected area.
                    cv2.rectangle(
                        org_image, pt, 
                        (pt[0] + target_w, pt[1] + target_h),
                        (0, 0, 255), 2
                    )
                    return True, org_image
        return False, org_image
