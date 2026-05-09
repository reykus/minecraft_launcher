import os
import sys
import json

def get_app_data_dir():
    """Повертає стандартну директорію для даних додатку залежно від ОС"""
    app_name = "ModernMCLauncher"
    
    if sys.platform == 'win32':
        # Windows: C:\Users\Користувач\AppData\Roaming\ModernMCLauncher
        base = os.getenv('APPDATA')
    elif sys.platform == 'darwin':
        # macOS: ~/Library/Application Support/ModernMCLauncher
        base = os.path.expanduser('~/Library/Application Support')
    else:
        # Linux: ~/.local/share/ModernMCLauncher
        base = os.getenv('XDG_DATA_HOME', os.path.expanduser('~/.local/share'))
        
    path = os.path.join(base, app_name)
    os.makedirs(path, exist_ok=True)
    return path

# Тепер DATA_DIR вказує на стандартну папку ОС
DATA_DIR = get_app_data_dir()
CONFIG_PATH = os.path.join(DATA_DIR, "config.json")

class ConfigManager:
    def __init__(self):
        self.config = self.load_config()

    def load_config(self):
        if not os.path.exists(CONFIG_PATH):
            return {
                "nickname": "Player",
                "ram_mb": 2048,
                "java_path": ""
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