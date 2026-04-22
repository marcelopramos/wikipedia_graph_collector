import json
import os

def save_json(data, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read().strip()

        if not content:
            return None

        return json.loads(content)