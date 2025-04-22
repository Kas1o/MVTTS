import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton,
    QLabel, QStackedWidget, QListWidget, QListWidgetItem, QHBoxLayout
)
from PySide6.QtCore import Qt
from gui.task_import_page import TaskImportPage
from gui.home_page import HomePage
from gui.work_page import WorkPage
from gui.insert_page import InsertPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RPG Maker MV TTS 配音工具")
        self.resize(900, 600)

        central_widget = QWidget()
        main_layout = QHBoxLayout()

        self.pages = QStackedWidget()
        self.page_names = ["首页", "任务导入", "工作区", "插入导出"]
        self.page_widgets = [HomePage(), TaskImportPage(), WorkPage(), InsertPage()]

        for widget in self.page_widgets:
            self.pages.addWidget(widget)

        nav_panel = self.create_navigation_panel()

        main_layout.addWidget(nav_panel)
        main_layout.addWidget(self.pages, stretch=1)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def create_navigation_panel(self):
        nav_widget = QWidget()
        layout = QVBoxLayout()
        list_widget = QListWidget()

        for name in self.page_names:
            list_widget.addItem(QListWidgetItem(name))

        list_widget.currentRowChanged.connect(self.pages.setCurrentIndex)
        layout.addWidget(QLabel("模块导航"))
        layout.addWidget(list_widget)
        layout.addStretch()
        nav_widget.setLayout(layout)
        return nav_widget


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
