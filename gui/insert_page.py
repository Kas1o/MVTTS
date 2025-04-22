from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
import os
import json
import shutil
from core.state import app_state


class InsertPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("插入与导出模块：将音频插入 RPG Maker MV 项目"))

        self.insert_button = QPushButton("插入音频并修改事件")
        self.insert_button.clicked.connect(self.insert_audio_and_modify_json)
        layout.addWidget(self.insert_button)

        self.setLayout(layout)

    def insert_audio_and_modify_json(self):
        project_path = app_state.project_path
        output_dir = os.path.join(project_path, "output")
        audio_dir = os.path.join(project_path, "audio", "se")
        os.makedirs(audio_dir, exist_ok=True)

        data_dir = os.path.join(project_path, "data")

        def insert_audio_command(audio_filename):
            return {
                "code": 250,
                "indent": 0,
                "parameters": [{
                    "name": audio_filename,
                    "volume": 90,
                    "pitch": 100,
                    "pan": 0
                }]
            }

        modified_files = set()

        # 处理 MapXXX.json
        for filename in os.listdir(data_dir):
            if not (filename.startswith("Map") and filename.endswith(".json")):
                continue
            if filename.endswith("MapInfos.json"):
                continue

            filepath = os.path.join(data_dir, filename)
            with open(filepath, encoding="utf-8-sig") as f:
                try:
                    json_data = json.load(f)
                except json.JSONDecodeError:
                    continue

            modified = False
            for event in json_data.get("events", []):
                if not event:
                    continue
                for page in event.get("pages", []):
                    event_list = page.get("list", [])
                    inserts = []
                    for i, cmd in enumerate(event_list):
                        if cmd.get("code") == 401:
                            text = cmd.get("parameters", [""])[0]
                            audio_path = app_state.audio_cache.get(text)
                            if audio_path:
                                se_name = os.path.splitext(os.path.basename(audio_path))[0]
                                target_path = os.path.join(audio_dir, se_name + ".ogg")
                                if not os.path.exists(target_path):
                                    shutil.copy(audio_path, target_path)

                                # 寻找 code 101 的位置
                                insert_index = i
                                for j in range(i - 1, -1, -1):
                                    if event_list[j].get("code") == 101:
                                        insert_index = j
                                        break
                                inserts.append((insert_index, insert_audio_command(se_name)))
                    for index, insert_cmd in reversed(inserts):
                        event_list.insert(index, insert_cmd)
                        modified = True
            if modified:
                with open(filepath, "w", encoding="utf-8-sig") as f:
                    json.dump(json_data, f, ensure_ascii=False, indent=2)
                modified_files.add(filename)

        # 处理 CommonEvents.json
        common_path = os.path.join(data_dir, "CommonEvents.json")
        if os.path.exists(common_path):
            try:
                with open(common_path, encoding="utf-8-sig") as f:
                    common_data = json.load(f)
            except json.JSONDecodeError:
                common_data = []

            modified = False
            for common_event in common_data:
                if not common_event:
                    continue
                event_list = common_event.get("list", [])
                inserts = []
                for i, cmd in enumerate(event_list):
                    if cmd.get("code") == 401:
                        text = cmd.get("parameters", [""])[0]
                        audio_path = app_state.audio_cache.get(text)
                        if audio_path:
                            se_name = os.path.splitext(os.path.basename(audio_path))[0]
                            target_path = os.path.join(audio_dir, se_name + ".ogg")
                            if not os.path.exists(target_path):
                                shutil.copy(audio_path, target_path)

                            insert_index = i
                            for j in range(i - 1, -1, -1):
                                if event_list[j].get("code") == 101:
                                    insert_index = j
                                    break
                            inserts.append((insert_index, insert_audio_command(se_name)))
                for index, insert_cmd in reversed(inserts):
                    event_list.insert(index, insert_cmd)
                    modified = True

            if modified:
                with open(common_path, "w", encoding="utf-8-sig") as f:
                    json.dump(common_data, f, ensure_ascii=False, indent=2)
                modified_files.add("CommonEvents.json")

        QMessageBox.information(self, "完成", f"插入完成，已修改 {len(modified_files)} 个文件。")
