import os
import json


def extract_dialogue_tasks_from_event_list(event_list, skip_if_has_se=False):
    tasks = []
    for i, cmd in enumerate(event_list):
        if cmd.get("code") == 401:
            text = cmd.get("parameters", [""])[0]
            if not text:
                continue
            if(text == ""):
                continue
            insert_index = i
            # 向前搜索 code 101
            for j in range(i - 1, -1, -1):
                if event_list[j].get("code") == 101:
                    insert_index = j
                    break

            if skip_if_has_se:
                # 在 insert_index 前检查是否存在 code 250
                for k in range(insert_index - 1, -1, -1):
                    if event_list[k].get("code") == 250:
                        break  # 有SE指令 → 跳过该任务
                else:
                    tasks.append({"text": text, "insert_index": insert_index})
            else:
                tasks.append({"text": text, "insert_index": insert_index})
    return tasks



def generate_tasks_from_project(project_root, skip_existing_se=False):
    tasks = []
    data_dir = os.path.join(project_root, "data")
    if not os.path.isdir(data_dir):
        return tasks

    # Map 文件处理
    for filename in os.listdir(data_dir):
        if filename.startswith("Map") and filename.endswith(".json"):
            if filename.endswith("MapInfos.json"):
                continue
            print("Try Reading " + os.path.join(data_dir, filename))
            with open(os.path.join(data_dir, filename), encoding="utf-8-sig") as f:
                try:
                    map_data = json.load(f)
                except json.JSONDecodeError:
                    continue
            for event in map_data.get("events", []):
                if not event:
                    continue
                for page in event.get("pages", []):
                    event_list = page.get("list", [])
                    event_tasks = extract_dialogue_tasks_from_event_list(
                        event_list, skip_if_has_se=skip_existing_se
                    )
                    tasks.extend(event_tasks)

    # CommonEvents 文件处理
    common_file = os.path.join(data_dir, "CommonEvents.json")
    if os.path.exists(common_file):
        with open(common_file, encoding="utf-8-sig") as f:
            try:
                common_events = json.load(f)
            except json.JSONDecodeError:
                common_events = []
        for common_event in common_events:
            if not common_event:
                continue
            event_list = common_event.get("list", [])
            event_tasks = extract_dialogue_tasks_from_event_list(
                event_list, skip_if_has_se=skip_existing_se
            )
            tasks.extend(event_tasks)

    return tasks
