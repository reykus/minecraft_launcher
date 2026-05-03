import os
import json

DATA_DIR = os.path.join(os.getcwd(), "data")
CONFIG_PATH = os.path.join(DATA_DIR, "config.json")

class ConfigManager:
    def __init__(self):
        os.makedirs(DATA_DIR, exist_ok=True)
        self.config = self.load_config()

    def load_config(self):
        if not os.path.exists(CONFIG_PATH):
            return {
                "nickname": "Player",
                "ram_mb": 2048,
                "java_path": "" # Поки пусто, додамо в фазі 2
            }
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_config(self):
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=4)

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value
        self.save_config()