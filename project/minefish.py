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
import sys
import setting
import image_detection
import window_manager
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QTabWidget, QVBoxLayout, QPushButton, QGridLayout, QCheckBox

SETTING_PATH = './setting.json'
FREQUENCY = 25
MIN_SCALE = 0.7
MAX_SCALE = 1.2
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
        self.search_window()

    def initialize_ui(self) -> None:
        self.capturing_label = QLabel('Searching for the Minecraft window...')
        self.capturing_label.setAlignment(Qt.AlignCenter)

        preview_tab = self.initialize_preview_tab()
        setting_tab = QWidget()
        about_tab = QWidget()

        self.main_tabs = QTabWidget()
        self.main_tabs.addTab(preview_tab, 'Preview')
        self.main_tabs.addTab(setting_tab, 'Setting')
        self.main_tabs.addTab(about_tab, 'About')

        box_layout = QVBoxLayout()
        box_layout.addWidget(self.capturing_label)
        box_layout.addWidget(self.main_tabs)

        self.setLayout(box_layout)
        self.setWindowTitle('MineFish')
        self.setGeometry(300, 300, WIDTH, HEIGHT)
        self.show()

    def initialize_preview_tab(self) -> 'QWidget()':
        preview_tab = QWidget()

        self.active_toggle = QCheckBox('Active')

        target_label = QLabel('Target Image')
        target_pixmap = QPixmap(self.setting.setting['image'])
        target_image = QLabel()
        target_image.setPixmap(target_pixmap)

        capture_label = QLabel('Captured Image')
        self.capture_image = QLabel()

        grid_layout = QGridLayout()
        grid_layout.addWidget(self.active_toggle, 0, 0)
        grid_layout.addWidget(target_label, 1, 0)
        grid_layout.addWidget(target_image, 2, 0)
        grid_layout.addWidget(capture_label, 3, 0)
        grid_layout.addWidget(self.capture_image, 4, 0)

        preview_tab.setLayout(grid_layout)

        return preview_tab

    def search_window(self) -> None:
        self.main_tabs.setVisible(False)
        self.capturing_label.setVisible(True)

        self.search_window_timer = QTimer()
        self.search_window_timer.setInterval(500)
        self.search_window_timer.timeout.connect(self.search_window_timer_event)
        self.search_window_timer.start()

    def search_window_timer_event(self) -> None:
        self.game_window = window_manager.get_matched_window(MATCH)
        if self.game_window != None:
            self.main_tabs.setVisible(True)
            self.capturing_label.setVisible(False)
            self.search_window_timer.stop()
            self.detect()

    def detect(self) -> None:
        delay = int(self.setting.setting['detection_delay'] * 1000)
        self.match_timer = QTimer()
        self.match_timer.setInterval(delay)
        self.match_timer.timeout.connect(self.detect_timer)
        self.match_timer.start()

    def detect_timer(self) -> None:
        left, top, width, height = window_manager.get_window_size(self.game_window)
        p1, p2 = self.image_detection.get_capture_points(left, top, width, height)

        org_image, gray_image = self.image_detection.capture_area(p1, p2)
        detected, org_image = self.image_detection.image_match(org_image, gray_image)

        self.capture_image.setPixmap(self.to_pixmap(org_image))

    def to_pixmap(self, image):
        qimg = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
        return QPixmap.fromImage(qimg)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MineFish()
    sys.exit(app.exec_())
