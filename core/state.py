class AppState:
    def __init__(self):
        self.tasks = []  # 所有任务 [{"text": ..., "insert_index": ...}]
        self.project_path = ""  # 当前项目路径
        self.audio_cache = {}  # text -> audio 文件名


# 单例
app_state = AppState()
