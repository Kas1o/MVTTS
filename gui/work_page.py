from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton, QHBoxLayout, QListWidgetItem, QMessageBox
from PySide6.QtGui import QColor
import os
from core.state import app_state
from core.tts_engine import generate_tts_audio
import hashlib
from tqdm import tqdm  # 确保导入 tqdm

def get_audio_output_path(text, output_dir, extension="wav"):
    os.makedirs(output_dir, exist_ok=True)
    key = text.encode("utf-8")
    filename = hashlib.md5(key).hexdigest() + "." + extension
    return os.path.join(output_dir, filename)


class WorkPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.addWidget(QLabel("工作区：TTS 生成与任务管理"))

        self.task_list = QListWidget()
        layout.addWidget(self.task_list)

        button_layout = QHBoxLayout()
        self.preview_button = QPushButton("试听音频")
        self.regenerate_button = QPushButton("重新生成")
        self.generate_all_button = QPushButton("生成全部")
        self.refresh_button = QPushButton("刷新任务")

        button_layout.addWidget(self.preview_button)
        button_layout.addWidget(self.regenerate_button)
        button_layout.addStretch()
        button_layout.addWidget(self.generate_all_button)
        button_layout.addWidget(self.refresh_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.refresh_button.clicked.connect(self.load_tasks)
        self.generate_all_button.clicked.connect(self.generate_all_missing)
        self.regenerate_button.clicked.connect(self.regenerate_selected)
        self.preview_button.clicked.connect(self.preview_selected)

        self.load_tasks()

    def load_tasks(self):
        self.task_list.clear()
        for task in app_state.tasks:
            text = task["text"]
            path = app_state.audio_cache.get(text)
            item = QListWidgetItem(text)
            if path and os.path.exists(path):
                item.setForeground(QColor("green"))
            else:
                item.setForeground(QColor("red"))
            self.task_list.addItem(item)

    def generate_audio_for_task(self, task):
        text = task["text"]
        output_dir = os.path.join(app_state.project_path, "output")
        file_path = get_audio_output_path(text, output_dir)

        if os.path.exists(file_path):
            app_state.audio_cache[text] = file_path
            return file_path

        audio_data = generate_tts_audio(text)
        if audio_data:
            with open(file_path, "wb") as f:
                f.write(audio_data)
                print("Saving file" + file_path)
            app_state.audio_cache[text] = file_path
            return file_path
        return None



    def generate_all_missing(self):
        count = 0
        # 使用 tqdm 包装任务列表以显示进度条
        for task in tqdm(app_state.tasks, desc="生成音频进度", unit="task"):
            text = task["text"]
            if text not in app_state.audio_cache or not os.path.exists(app_state.audio_cache[text]):
                if self.generate_audio_for_task(task):
                    count += 1
        QMessageBox.information(self, "完成", f"生成完成，共生成 {count} 个音频文件。")
        self.load_tasks()

    def regenerate_selected(self):
        item = self.task_list.currentItem()
        if not item:
            return
        text = item.text()
        task = next((t for t in app_state.tasks if t["text"] == text), None)
        if not task:
            return

        output_dir = os.path.join(app_state.project_path, "output")
        file_path = get_audio_output_path(text, output_dir)
        audio_data = generate_tts_audio(text)
        if audio_data:
            with open(file_path, "wb") as f:
                f.write(audio_data)
            app_state.audio_cache[text] = file_path
            QMessageBox.information(self, "完成", "音频已重新生成。")
        self.load_tasks()

    def preview_selected(self):
        import subprocess

        item = self.task_list.currentItem()
        if not item:
            return
        text = item.text()
        path = app_state.audio_cache.get(text)
        if path and os.path.exists(path):
            subprocess.Popen(["ffplay", "-nodisp", "-autoexit", path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            QMessageBox.warning(self, "错误", "未找到音频文件，请先生成。")
