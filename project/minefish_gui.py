# minefish_gui.py
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

# https://wikidocs.net/21849

import os
import sys
import json
import minefish
import pyautogui
import webbrowser
import pygetwindow
from shutil import copyfile
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QImage, QPixmap, QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QWidget,
    QTabWidget,
    QVBoxLayout,
    QPushButton,
    QGridLayout,
    QCheckBox,
    QComboBox,
    QSlider,
    QFileDialog
)
from qt_material import apply_stylesheet

VERSION = '4.0.0'

WIDTH = 600
HEIGHT = 400
IMAGE_PATH = '.\\image'
LANGUAGE_PATH = '.\\language'
ICON_PATH = '.\\resources\\icon.png'
LOGO_PATH = '.\\resources\\MineFish.png'
INITIAL_SETTING = {
    'accuracy': 0.7,
   	'detection_delay': 0.3,
   	'throwing_delay': 0.5,
   	'frequency': 40,
   	'min_scale': 0.5,
   	'max_scale': 2.0
}

class MineFishGUI(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.minefish = minefish.MineFish()

        self.initialize_ui()
        self.set_preview_active()
        self.load_resources()
        self.load_language()

        self.search_window()
        self.show()

# region Initialize UI

    def initialize_ui(self) -> None:
        apply_stylesheet(self, theme='dark_lightgreen.xml')

        preview_tab = self.initialize_preview_tab()
        setting_tab = self.initialize_setting_tab()
        about_tab = self.initialize_about_tab()

        self.main_tabs = QTabWidget()
        self.main_tabs.addTab(preview_tab, 'preview')
        self.main_tabs.addTab(setting_tab, 'setting')
        self.main_tabs.addTab(about_tab, 'about')

        box_layout = QVBoxLayout()
        box_layout.addWidget(self.main_tabs)

        self.setLayout(box_layout)
        self.setWindowTitle('MineFish')
        self.setWindowIcon(QIcon(ICON_PATH))
        self.setGeometry(300, 300, WIDTH, HEIGHT)

    # region Initialize Preview Tab

    def initialize_preview_tab(self) -> QWidget:
        preview_tab = QWidget()

        self.capturing_label = QLabel('capturing_label')
        self.capturing_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.active_toggle = QCheckBox('active_toggle')
        self.active_toggle.setChecked(False)
        self.active_toggle.stateChanged.connect(self.set_preview_active)

        self.target_label = QLabel('target_label')
        self.target_image = QLabel()

        self.capture_label = QLabel('capture_label')
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
        state = self.active_toggle.isChecked()
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

    # endregion

    # region Initialize Setting Tab

    def initialize_setting_tab(self) -> QWidget:
        setting_tab = QWidget()

        # Target Image
        self.target_image_title = QLabel('target_image_title')
        self.target_image_list = QComboBox()
        self.target_image_list.activated.connect(self.setting_combobox_item_change_event)
        self.target_image_dialog_button = QPushButton('target_image_dialog_button')
        self.target_image_dialog_button.clicked.connect(self.target_image_add_file_dialog)
        self.target_image_folder_button = QPushButton('target_image_folder_button')
        self.target_image_folder_button.clicked.connect(self.target_image_open_folder)

        target_image_box_layout = QGridLayout()
        target_image_box_layout.addWidget(self.target_image_title, 0, 0)
        target_image_box_layout.addWidget(self.target_image_list, 1, 0, 1, 8)
        target_image_box_layout.addWidget(self.target_image_dialog_button, 1, 9, 1, 1)
        target_image_box_layout.addWidget(self.target_image_folder_button, 1, 10, 1, 1)

        # Display Language
        self.language_title = QLabel('language_title')
        self.language_list = QComboBox()
        self.language_list.activated.connect(self.setting_combobox_item_change_event)

        slider_grid = QGridLayout()
        slider_grid.addLayout(self.initialize_normal_setting_box(), 0, 0)
        slider_grid.addLayout(self.initialize_advanced_setting_box(), 0, 1)

        self.refresh_button = QPushButton('refresh_button')
        self.refresh_button.clicked.connect(self.load_resources)

        self.reset_button = QPushButton('reset_button')
        self.reset_button.clicked.connect(self.reset_setting)

        toolbar_layout = QHBoxLayout()
        toolbar_layout.addWidget(self.refresh_button)
        toolbar_layout.addWidget(self.reset_button)

        box_layout = QVBoxLayout()
        box_layout.addLayout(target_image_box_layout)
        box_layout.addStretch(1)
        box_layout.addWidget(self.language_title)
        box_layout.addWidget(self.language_list)
        box_layout.addStretch(1)
        box_layout.addLayout(slider_grid)
        box_layout.addStretch(1)
        box_layout.addLayout(toolbar_layout)
        setting_tab.setLayout(box_layout)

        return setting_tab

    def initialize_normal_setting_box(self) -> QVBoxLayout:
        # Accuracy
        self.accuracy_title = QLabel('accuracy_title')
        self.accuracy_value = QLabel()
        self.accuracy_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.accuracy_bar = QSlider(Qt.Orientation.Horizontal)
        self.accuracy_bar.setRange(30, 90)
        self.accuracy_bar.valueChanged.connect(
            self.create_setting_slider_event(
                value_display=self.accuracy_value,
                key='accuracy',
                scale=100,
                value_type=float
            )
        )

        # Detection Delay
        self.detection_title = QLabel('detection_title')
        self.detection_value = QLabel()
        self.detection_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.detection_bar = QSlider(Qt.Orientation.Horizontal)
        self.detection_bar.setRange(10, 50)
        self.detection_bar.valueChanged.connect(
            self.create_setting_slider_event(
                value_display=self.detection_value,
                key='detection_delay',
                scale=100,
                value_type=float
            )
        )

        # Throwing Delay
        self.throwing_title = QLabel('throwing_title')
        self.throwing_value = QLabel()
        self.throwing_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.throwing_bar = QSlider(Qt.Orientation.Horizontal)
        self.throwing_bar.setRange(30, 500)
        self.throwing_bar.valueChanged.connect(
            self.create_setting_slider_event(
                value_display=self.throwing_value,
                key='throwing_delay',
                scale=100,
                value_type=float
            )
        )

        normal_box = QVBoxLayout()
        normal_box.addWidget(self.accuracy_title)
        normal_box.addWidget(self.accuracy_bar)
        normal_box.addWidget(self.accuracy_value)
        normal_box.addStretch(1)
        normal_box.addWidget(self.detection_title)
        normal_box.addWidget(self.detection_bar)
        normal_box.addWidget(self.detection_value)
        normal_box.addStretch(1)
        normal_box.addWidget(self.throwing_title)
        normal_box.addWidget(self.throwing_bar)
        normal_box.addWidget(self.throwing_value)

        return normal_box

    def initialize_advanced_setting_box(self) -> QVBoxLayout:
        # Frequency
        self.frequency_title = QLabel('frequency_title')
        self.frequency_value = QLabel()
        self.frequency_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.frequency_bar = QSlider(Qt.Orientation.Horizontal)
        self.frequency_bar.setRange(10, 100)
        self.frequency_bar.valueChanged.connect(
            self.create_setting_slider_event(
                value_display=self.frequency_value,
                key='frequency',
                scale=1,
                value_type=int
            )
        )

        # Min Scale
        self.min_scale_title = QLabel('min_scale_title')
        self.min_scale_value = QLabel()
        self.min_scale_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.min_scale_bar = QSlider(Qt.Orientation.Horizontal)
        self.min_scale_bar.setRange(10, 80)
        self.min_scale_bar.valueChanged.connect(
            self.create_setting_slider_event(
                value_display=self.min_scale_value,
                key='min_scale',
                scale=100,
                value_type=float
            )
        )

        # Max Scale
        self.max_scale_title = QLabel('max_scale_title')
        self.max_scale_value = QLabel()
        self.max_scale_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.max_scale_bar = QSlider(Qt.Orientation.Horizontal)
        self.max_scale_bar.setRange(90, 250)
        self.max_scale_bar.valueChanged.connect(
            self.create_setting_slider_event(
                value_display=self.max_scale_value,
                key='max_scale',
                scale=100,
                value_type=float
            )
        )

        advanced_box = QVBoxLayout()
        advanced_box.addWidget(self.frequency_title)
        advanced_box.addWidget(self.frequency_bar)
        advanced_box.addWidget(self.frequency_value)
        advanced_box.addStretch(1)
        advanced_box.addWidget(self.min_scale_title)
        advanced_box.addWidget(self.min_scale_bar)
        advanced_box.addWidget(self.min_scale_value)
        advanced_box.addStretch(1)
        advanced_box.addWidget(self.max_scale_title)
        advanced_box.addWidget(self.max_scale_bar)
        advanced_box.addWidget(self.max_scale_value)

        return advanced_box

    def create_setting_slider_event(self, value_display: QLabel, key: str, scale: int, value_type: 'function') -> 'function':
        def setting_slider_event(value: int) -> None:
            new_value = value_type(value / scale)
            value_display.setText(str(new_value))
            self.minefish.setting[key] = new_value
            self.minefish.save_setting()
        return setting_slider_event

    def setting_combobox_item_change_event(self) -> None:
        self.minefish.setting['image'] = self.target_image_list.currentText()
        self.minefish.setting['display_language'] = self.language_list.currentText()
        self.minefish.save_setting()
        self.load_resources()
        self.load_language()

    def target_image_add_file_dialog(self) -> None:
        new_image_path = QFileDialog.getOpenFileName(self, 'Add File', './')[0]
        image_name = os.path.basename(new_image_path)
        copyfile(new_image_path, f'{IMAGE_PATH}\\{image_name}')
        self.load_resources()

    def target_image_open_folder(self) -> None:
        os.startfile(IMAGE_PATH)

    # endregion

    # region Initialize About Tab

    def initialize_about_tab(self) -> QWidget:
        about_tab = QWidget()

        logo_image = QLabel()
        logo_pixmap = QPixmap(LOGO_PATH)
        logo_image.setPixmap(logo_pixmap)
        logo_image.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        copyright_label = QLabel('Copyright 2020 Nitro. All Rights Reserved.')

        developer_layout = self.create_clickable_label('Developer:', 'Nitro (admin@nitrostudio.dev)', 'mailto:admin@nitrostudio.dev')
        blog_layout = self.create_clickable_label('Blog:', 'https://blog.nitrostudio.dev', 'https://blog.nitrostudio.dev')
        discord_layout = self.create_clickable_label('Discord:', 'https://discord.nitrostudio.dev', 'https://discord.nitrostudio.dev')
        gitHub_layout = self.create_clickable_label('GitHub:', 'https://github.com/Nitro1231/MineFish', 'https://github.com/Nitro1231/MineFish')
        version_layout = self.create_clickable_label('Version:', VERSION, 'https://github.com/Nitro1231/MineFish/releases')

        self.update_state_label = QLabel('Checking for a new update...')

        self.text_label = QLabel('Thank you for using MineFish. You are always welcome to give us any feedback or share amazing ideas about MineFish. Feel free to join my Discord Server! Thank you :)')
        self.text_label.setWordWrap(True)

        box_layout = QVBoxLayout()
        box_layout.addWidget(logo_image)
        box_layout.addWidget(copyright_label)
        box_layout.addLayout(developer_layout)
        box_layout.addLayout(blog_layout)
        box_layout.addLayout(discord_layout)
        box_layout.addLayout(gitHub_layout)
        box_layout.addLayout(version_layout)
        box_layout.addWidget(self.update_state_label)
        box_layout.addWidget(self.text_label)
        box_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        about_tab.setLayout(box_layout)

        return about_tab

    def create_clickable_label(self, name: str, value: str, link: str) -> QHBoxLayout:
        box_layout = QHBoxLayout()
        name_label = QLabel(name)
        value_label = QLabel(value)
        value_label.setStyleSheet('color: #8bc34a')

        def open_link(event):
            webbrowser.open(link)
        
        value_label.mousePressEvent = open_link

        box_layout.addWidget(name_label)
        box_layout.addWidget(value_label)
        box_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        return box_layout

    # endregion

# endregion

# region Timer

    def search_window(self) -> None:
        self.set_preview_visibility(False)
        self.search_window_timer = self.make_timer(500, self.search_window_timer_event)
        self.search_window_timer.start()

    def search_window_timer_event(self) -> None:
        self.minefish.select_matched_window()
        if self.minefish.game_window != None:
            self.active_toggle.setCheckState(Qt.CheckState.Checked)
            self.set_preview_visibility(True)
            self.search_window_timer.stop()

    def detect(self, state: bool) -> None:
        interval = int(self.minefish.setting['detection_delay'] * 1000)
        self.detect_timer = self.make_timer(interval, self.detect_timer_event)

        if state:
            self.detect_timer.start()
        else:
            self.detect_timer.stop()

    def detect_timer_event(self) -> None:
        try:
            detected, org_image = self.minefish.detect()
            self.capture_image.setPixmap(self.to_pixmap(org_image))
            if detected:
                self.throw_rod()
        except pygetwindow.PyGetWindowException:
            self.active_toggle.setCheckState(Qt.CheckState.Unchecked)
            self.search_window()

    def throw_rod(self) -> None:
        self.detect_timer.stop()
        pyautogui.click(button='right')
        interval = int(self.minefish.setting['throwing_delay'] * 1000)
        self.throw_timer = self.make_timer(interval, self.throw_timer_event)
        self.throw_timer.start()

    def throw_timer_event(self) -> None:
        pyautogui.click(button='right')
        self.delay_timer = self.make_timer(4000, self.delay_timer_event)
        self.delay_timer.start()
        self.throw_timer.stop()

    def delay_timer_event(self) -> None:
        self.detect_timer.start()
        self.delay_timer.stop()

    def make_timer(self, interval: int, event: 'function') -> QTimer:
        timer = QTimer()
        timer.setInterval(interval)
        timer.timeout.connect(event)
        return timer

# endregion

# region Extra Functionalities

    def load_resources(self) -> None:
        self.minefish.load_setting()
        self.minefish.load_target_image()
        self.target_pixmap = QPixmap(self.minefish.setting['image'])
        self.target_image.setPixmap(self.target_pixmap)
        self.target_image_list.clear()
        self.language_list.clear()
        self.target_image_list.addItems(self.get_files(IMAGE_PATH))
        self.language_list.addItems(self.get_files(LANGUAGE_PATH))
        self.set_combobox_item(self.target_image_list, self.minefish.setting['image'])
        self.set_combobox_item(self.language_list, self.minefish.setting['display_language'])
        self.accuracy_bar.setValue(int(self.minefish.setting['accuracy'] * 100))
        self.detection_bar.setValue(int(self.minefish.setting['detection_delay'] * 100))
        self.throwing_bar.setValue(int(self.minefish.setting['throwing_delay'] * 100))
        self.frequency_bar.setValue(self.minefish.setting['frequency'])
        self.min_scale_bar.setValue(int(self.minefish.setting['min_scale'] * 100))
        self.max_scale_bar.setValue(int(self.minefish.setting['max_scale'] * 100))

    def load_language(self) -> None:
        with open(self.minefish.setting['display_language'], 'r', encoding='utf-8') as f:
            lang = json.load(f)

        # main_tabs
        self.main_tabs.setTabText(0, lang['tabs']['preview'])
        self.main_tabs.setTabText(1, lang['tabs']['setting'])
        self.main_tabs.setTabText(2, lang['tabs']['about'])

        # preview_tab
        self.capturing_label.setText(lang['preview_tab']['capturing_label'])
        self.active_toggle.setText(lang['preview_tab']['active_toggle'])
        self.target_label.setText(lang['preview_tab']['target_label'])
        self.capture_label.setText(lang['preview_tab']['capture_label'])

        # setting_tab
        self.target_image_title.setText(lang['setting_tab']['target_image_title'])
        self.target_image_dialog_button.setText(lang['setting_tab']['target_image_dialog_button'])
        self.target_image_folder_button.setText(lang['setting_tab']['target_image_folder_button'])
        self.language_title.setText(lang['setting_tab']['language_title'])
        self.refresh_button.setText(lang['setting_tab']['refresh_button'])
        self.reset_button.setText(lang['setting_tab']['reset_button'])

        # normal_setting_box
        self.accuracy_title.setText(lang['setting_tab']['accuracy_title'])
        self.detection_title.setText(lang['setting_tab']['detection_title'])
        self.throwing_title.setText(lang['setting_tab']['throwing_title'])

        # advanced_setting_box
        self.frequency_title.setText(lang['setting_tab']['frequency_title'])
        self.min_scale_title.setText(lang['setting_tab']['min_scale_title'])
        self.max_scale_title.setText(lang['setting_tab']['max_scale_title'])

        # about_tab
        self.update_state_label.setText(lang['about_tab']['update_state_label']['checking'])
        self.text_label.setText(lang['about_tab']['text_label'])

    def set_combobox_item(self, combobox: QComboBox, text: str) -> None:
        index = combobox.findText(text, Qt.MatchFlag.MatchFixedString)
        if index >= 0:
            combobox.setCurrentIndex(index)

    def get_files(self, path: str) -> list():
        files = list()
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isfile(item_path):
                files.append(item_path)
        return files

    def reset_setting(self) -> None:
        for key in INITIAL_SETTING:
            self.minefish.setting[key] = INITIAL_SETTING[key]
        self.minefish.save_setting()
        self.load_resources()

    def to_pixmap(self, image) -> QPixmap:
        height, width, channel = image.shape
        bytesPerLine = 3 * width
        qimg = QImage(
            image.data, width, height,
            bytesPerLine, QImage.Format.Format_RGB888
        )
        return QPixmap.fromImage(qimg)

# endregion

if __name__ == '__main__':
    # try:
    app = QApplication(sys.argv)
    ex = MineFishGUI()
    sys.exit(app.exec())
    # except Exception as e:
