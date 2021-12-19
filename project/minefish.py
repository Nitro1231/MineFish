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
import sys
import setting
import image_detection
import window_manager
import pygetwindow
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QWidget,
    QTabWidget,
    QVBoxLayout,
    QPushButton,
    QGridLayout,
    QCheckBox,
    QComboBox,
    QSlider
)
from qt_material import apply_stylesheet

SETTING_PATH = '.\\setting.json'
IMAGE_PATH = '.\\image'
LANGUAGE_PATH = '.\\language'
WIDTH = 600
HEIGHT = 400
MATCH = {
    'include': ['Minecraft'],
    'exclude': ['Launcher', 'Updater']  # Launcher
}


class MineFish(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setting = setting.Setting(SETTING_PATH)

        self.initialize_ui()
        self.set_preview_active()
        self.load_resources()
        self.load_language()

        self.search_window()

    def initialize_ui(self) -> None:
        apply_stylesheet(self, theme='dark_lightgreen.xml')

        preview_tab = self.initialize_preview_tab()
        setting_tab = self.initialize_setting_tab()
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

        box_layout = QVBoxLayout()
        box_layout.addWidget(self.capturing_label)
        box_layout.addWidget(self.active_toggle)
        box_layout.addWidget(self.target_label)
        box_layout.addWidget(self.target_image)
        box_layout.addWidget(self.capture_label)
        box_layout.addWidget(self.capture_image)
        preview_tab.setLayout(box_layout)

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

        # Target Image
        target_image_title = QLabel('Target Image')
        target_image_list = QComboBox()
        target_image_list.addItems(self.get_files(IMAGE_PATH))
        target_image_dialog_button = QPushButton('Open File')
        target_image_folder_button = QPushButton('Open Folder')
        
        target_image_box_layout = QGridLayout()
        target_image_box_layout.addWidget(target_image_title, 0, 0)
        target_image_box_layout.addWidget(target_image_list, 1, 0, 1, 8)
        target_image_box_layout.addWidget(target_image_dialog_button, 1, 9, 1, 1)
        target_image_box_layout.addWidget(target_image_folder_button, 1, 10, 1, 1)

        # Display Language
        language_title = QLabel('Display Language')
        language_list = QComboBox()
        language_list.addItems(self.get_files(LANGUAGE_PATH))

        # normal_box
        # Accuracy
        accuracy_title = QLabel('Accuracy')
        accuracy_value = QLabel()
        accuracy_value.setAlignment(Qt.AlignCenter)
        accuracy_bar = QSlider(Qt.Horizontal)
        accuracy_bar.setRange(30, 90)
        accuracy_bar.valueChanged.connect(
            self.make_slider_event(
                value_display=accuracy_value,
                key='accuracy',
                scale=100,
                value_type=float
            )
        )

        # Detection Delay
        detection_title = QLabel('Detection Delay')
        detection_value = QLabel()
        detection_value.setAlignment(Qt.AlignCenter)
        detection_bar = QSlider(Qt.Horizontal)
        detection_bar.setRange(10, 50)
        detection_bar.valueChanged.connect(
            self.make_slider_event(
                value_display=detection_value,
                key='detection_delay',
                scale=100,
                value_type=float
            )
        )

        # Throwing Delay
        throwing_title = QLabel('Throwing Delay')
        throwing_value = QLabel()
        throwing_value.setAlignment(Qt.AlignCenter)
        throwing_bar = QSlider(Qt.Horizontal)
        throwing_bar.setRange(30, 500)
        throwing_bar.valueChanged.connect(
            self.make_slider_event(
                value_display=throwing_value,
                key='throwing_delay',
                scale=100,
                value_type=float
            )
        )

        normal_box = QVBoxLayout()
        normal_box.addWidget(accuracy_title)
        normal_box.addWidget(accuracy_bar)
        normal_box.addWidget(accuracy_value)
        normal_box.addStretch(1)
        normal_box.addWidget(detection_title)
        normal_box.addWidget(detection_bar)
        normal_box.addWidget(detection_value)
        normal_box.addStretch(1)
        normal_box.addWidget(throwing_title)
        normal_box.addWidget(throwing_bar)
        normal_box.addWidget(throwing_value)

        # advanced_box
        # Frequency
        frequency_title = QLabel('Frequency')
        frequency_value = QLabel()
        frequency_value.setAlignment(Qt.AlignCenter)
        frequency_bar = QSlider(Qt.Horizontal)
        frequency_bar.setRange(10, 100)
        frequency_bar.valueChanged.connect(
            self.make_slider_event(
                value_display=frequency_value,
                key='frequency',
                scale=1,
                value_type=int
            )
        )

        # Min Scale
        min_scale_title = QLabel('Min Scale')
        min_scale_value = QLabel()
        min_scale_value.setAlignment(Qt.AlignCenter)
        min_scale_bar = QSlider(Qt.Horizontal)
        min_scale_bar.setRange(10, 80)
        min_scale_bar.valueChanged.connect(
            self.make_slider_event(
                value_display=min_scale_value,
                key='min_scale',
                scale=100,
                value_type=float
            )
        )
        
        # Max Scale
        max_scale_title = QLabel('Max Scale')
        max_scale_value = QLabel()
        max_scale_value.setAlignment(Qt.AlignCenter)
        max_scale_bar = QSlider(Qt.Horizontal)
        max_scale_bar.setRange(90, 250)
        max_scale_bar.valueChanged.connect(
            self.make_slider_event(
                value_display=max_scale_value,
                key='max_scale',
                scale=100,
                value_type=float
            )
        )

        advanced_box = QVBoxLayout()
        advanced_box.addWidget(frequency_title)
        advanced_box.addWidget(frequency_bar)
        advanced_box.addWidget(frequency_value)
        advanced_box.addStretch(1)
        advanced_box.addWidget(min_scale_title)
        advanced_box.addWidget(min_scale_bar)
        advanced_box.addWidget(min_scale_value)
        advanced_box.addStretch(1)
        advanced_box.addWidget(max_scale_title)
        advanced_box.addWidget(max_scale_bar)
        advanced_box.addWidget(max_scale_value)

        slider_grid = QGridLayout()
        slider_grid.addLayout(normal_box, 0, 0)
        slider_grid.addLayout(advanced_box, 0, 1)

        box_layout = QVBoxLayout()
        box_layout.addLayout(target_image_box_layout)
        box_layout.addStretch(1)
        box_layout.addWidget(language_title)
        box_layout.addWidget(language_list)
        box_layout.addStretch(1)
        box_layout.addLayout(slider_grid)

        setting_tab.setLayout(box_layout)
        
        return setting_tab

    def make_slider_event(self, value_display: 'QLabel()', key: str, scale: int, value_type: 'function') -> 'function':
        def slider_event(value: int) -> None:
            new_value = value_type(value / scale)
            value_display.setText(str(new_value))
            self.setting.setting[key] = new_value
        return slider_event

    def get_files(self, path: str) -> list():
        files = list()
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isfile(item_path):
                files.append(item_path)
        return files

    def load_resources(self) -> None:
        self.image_detection = image_detection.ImageDetection(
            target_path=self.setting.setting['image'],
            accuracy=self.setting.setting['accuracy'],
            frequency=self.setting.setting['frequency'],
            min_scale=self.setting.setting['min_scale'],
            max_scale=self.setting.setting['max_scale']
        )

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
