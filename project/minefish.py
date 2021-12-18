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

# https://wikidocs.net/21849

import os
import cv2
import sys
import setting
import image_detection
import window_manager
import pygetwindow
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QTabWidget, QVBoxLayout, QPushButton, QGridLayout, QCheckBox
from qt_material import apply_stylesheet

SETTING_PATH = './setting.json'
FREQUENCY = 40
MIN_SCALE = 0.5
MAX_SCALE = 2.0
WIDTH = 600
HEIGHT = 400
MATCH = {
    'include': ['Minecraft'],
    'exclude': ['Updater']  # Launcher
}


class MineFish(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setting = setting.Setting(SETTING_PATH)
        self.setting.verify_setting()

        self.image_detection = image_detection.ImageDetection(
            target_path=self.setting.setting['image'],
            accuracy=self.setting.setting['accuracy'],
            frequency=FREQUENCY,
            min_scale=MIN_SCALE,
            max_scale=MAX_SCALE
        )

        self.initialize_ui()
        self.set_preview_active()
        self.load_resources()
        self.load_language()

        self.search_window()

    def initialize_ui(self) -> None:
        apply_stylesheet(self, theme='dark_lightgreen.xml')

        preview_tab = self.initialize_preview_tab()
        setting_tab = QWidget()
        about_tab = QWidget()

        main_tabs = QTabWidget()
        main_tabs.addTab(preview_tab, 'Preview')
        main_tabs.addTab(setting_tab, 'Setting')
        main_tabs.addTab(about_tab, 'About')

        box_layout = QVBoxLayout()
        box_layout.addWidget(main_tabs)

        self.setLayout(box_layout)
        self.setWindowTitle('MineFish')
        self.setGeometry(300, 300, WIDTH, HEIGHT)
        self.show()

    def initialize_preview_tab(self) -> 'QWidget()':
        preview_tab = QWidget()

        self.capturing_label = QLabel('Searching for the Minecraft window...')
        self.capturing_label.setAlignment(Qt.AlignCenter)

        self.active_toggle = QCheckBox('Active')
        self.active_toggle.setChecked(False)
        self.active_toggle.stateChanged.connect(self.set_preview_active)

        self.target_label = QLabel('Target Image')
        self.target_image = QLabel()

        self.capture_label = QLabel('Captured Image')
        self.capture_image = QLabel()

        grid_layout = QGridLayout()
        grid_layout.addWidget(self.capturing_label, 0, 0)
        grid_layout.addWidget(self.active_toggle, 0, 0)
        grid_layout.addWidget(self.target_label, 1, 0)
        grid_layout.addWidget(self.target_image, 2, 0)
        grid_layout.addWidget(self.capture_label, 3, 0)
        grid_layout.addWidget(self.capture_image, 4, 0)

        preview_tab.setLayout(grid_layout)

        return preview_tab

    def set_preview_active(self) -> None:
        state = self.active_toggle.checkState()
        self.target_label.setEnabled(state)
        self.target_image.setEnabled(state)
        self.capture_label.setEnabled(state)
        self.capture_image.setEnabled(state)

        self.detect(state)

    def set_preview_visibility(self, state: bool) -> None:
        self.active_toggle.setVisible(state)
        self.target_label.setVisible(state)
        self.target_image.setVisible(state)
        self.capture_label.setVisible(state)
        self.capture_image.setVisible(state)
        self.capturing_label.setVisible(not state)

    def initialize_setting_tab(self):
        setting_tab = QWidget()


        grid_layout = QGridLayout()
        grid_layout.addWidget(self.capturing_label, 0, 0)

        setting_tab.setLayout(grid_layout)

        return setting_tab

    def load_resources(self) -> None:
        self.target_pixmap = QPixmap(self.setting.setting['image'])
        self.target_image.setPixmap(self.target_pixmap)

    def load_language(self) -> None:
        pass

    def search_window(self) -> None:
        self.set_preview_visibility(False)

        self.search_window_timer = QTimer()
        self.search_window_timer.setInterval(500)
        self.search_window_timer.timeout.connect(self.search_window_timer_event)
        self.search_window_timer.start()

    def search_window_timer_event(self) -> None:
        self.game_window = window_manager.get_matched_window(MATCH)
        if self.game_window != None:
            self.set_preview_visibility(True)
            self.search_window_timer.stop()

    def detect(self, state: bool) -> None:
        delay = int(self.setting.setting['detection_delay'] * 1000)
        self.detect_timer = QTimer()
        self.detect_timer.setInterval(delay)
        self.detect_timer.timeout.connect(self.detect_timer_event)

        if state:
            self.detect_timer.start()
        else:
            self.detect_timer.stop()

    def detect_timer_event(self) -> None:
        try:
            left, top, width, height = window_manager.get_window_size(self.game_window)
            p1, p2 = self.image_detection.get_capture_points(left, top, width, height)

            org_image, gray_image = self.image_detection.capture_area(p1, p2)
            detected, org_image = self.image_detection.image_match(org_image, gray_image)

            self.capture_image.setPixmap(self.to_pixmap(org_image))
        except pygetwindow.PyGetWindowException:
            self.active_toggle.setCheckState(False)
            self.set_preview_visibility(False)
            self.search_window()

    def to_pixmap(self, image):
        height, width, channel = image.shape
        bytesPerLine = 3 * width
        qimg = QImage(image.data, width, height, bytesPerLine, QImage.Format_RGB888)
        return QPixmap.fromImage(qimg)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MineFish()
    sys.exit(app.exec_())
