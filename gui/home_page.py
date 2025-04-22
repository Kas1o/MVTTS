import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton,
    QLabel, QStackedWidget, QListWidget, QListWidgetItem, QHBoxLayout,
    QLineEdit, QFileDialog
)
from PySide6.QtCore import Qt


class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("欢迎使用 RPG Maker MV TTS 配音生成器"))
        layout.addStretch()
        self.setLayout(layout)