import event
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QLabel,
    QWidget,
    QVBoxLayout,
    QPlainTextEdit
)
from qt_material import apply_stylesheet


ICON_PATH = '.\\resources\\icon.png'


class UpdateGUI(QWidget):
    def __init__(self, minefish, info):
        super().__init__()
        self.minefish = minefish
        self.info = info
        self.initialize_ui()

        event.Event().link(self.load_language)
        event.Event().call()

        self.show()

    def initialize_ui(self) -> None:
        apply_stylesheet(self, theme='dark_lightgreen.xml')

        self.update_label = QLabel('update_label')
        self.update_label.setStyleSheet('font-size: 18pt; font-weight: bold; color: #8bc34a')
        self.version_label = QLabel('version_label')
        self.release_date_label = QLabel('release_date_label')
        # self.url_label = QLabel('url')
        self.description_label = QLabel('description_label')

        self.textedit_box = QPlainTextEdit('a')
        self.textedit_box.setReadOnly(True)

        box_layout = QVBoxLayout() 
        box_layout.addWidget(self.update_label)
        box_layout.addWidget(self.version_label)
        box_layout.addWidget(self.release_date_label)
        # box_layout.addWidget(self.url_label)
        box_layout.addWidget(self.description_label)
        box_layout.addWidget(self.textedit_box)
        box_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.setLayout(box_layout)
        self.setWindowTitle('MineFish')
        self.setWindowIcon(QIcon(ICON_PATH))

    def load_language(self) -> None:
        lang = self.minefish.lang

        self.update_label.setText(lang['update_window']['update_label'])
        self.version_label.setText(lang['update_window']['version_label'] + self.info['version'])
        self.release_date_label.setText(lang['update_window']['release_date_label'] + self.info['release_date'])
        # self.url_label.setText(f'URL: {self.info["url"]}')
        self.description_label.setText(lang['update_window']['description_label'])
        self.textedit_box.setPlainText(self.info['description'])
