import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog,
    QListWidget, QLineEdit, QHBoxLayout, QMessageBox, QCheckBox
)
from core.task_generator import generate_tasks_from_project
from core.state import app_state

class TaskImportPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("任务导入与生成模块"))

        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("请选择 RPG Maker MV 项目的根目录")
        layout.addWidget(self.path_input)

        self.browse_button = QPushButton("选择目录")
        self.browse_button.clicked.connect(self.browse_folder)
        layout.addWidget(self.browse_button)

        self.import_button = QPushButton("导入任务")
        self.import_button.clicked.connect(self.import_tasks)
        layout.addWidget(self.import_button)

        # 在 __init__ 中添加两个复选框，默认勾选
        self.skip_existing_checkbox = QCheckBox("忽略已有音频的对话")
        self.skip_existing_checkbox.setChecked(True)
        layout.addWidget(self.skip_existing_checkbox)

        self.load_cache_checkbox = QCheckBox("加载 output 音频缓存")
        self.load_cache_checkbox.setChecked(True)
        layout.addWidget(self.load_cache_checkbox)


        layout.addStretch()
        self.setLayout(layout)

    def browse_folder(self):
        path = QFileDialog.getExistingDirectory(self, "选择项目根目录")
        if path:
            self.path_input.setText(path)

    def import_tasks(self):
        root_path = self.path_input.text()
        if not os.path.isdir(root_path):
            print("路径无效")
            return

        skip_se = self.skip_existing_checkbox.isChecked()
        tasks = generate_tasks_from_project(root_path, skip_existing_se=skip_se)
        app_state.tasks = tasks
        app_state.project_path = root_path
        print(f"导入任务数: {len(tasks)}")

