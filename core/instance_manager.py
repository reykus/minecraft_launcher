import os
import json
import shutil
from utils.settings import DATA_DIR

INSTANCES_DIR = os.path.join(DATA_DIR, "instances")

class InstanceManager:
    def __init__(self):
        os.makedirs(INSTANCES_DIR, exist_ok=True)

    def get_all_instances(self):
        instances = []
        for dir_name in os.listdir(INSTANCES_DIR):
            instance_path = os.path.join(INSTANCES_DIR, dir_name)
            json_path = os.path.join(instance_path, "instance.json")
            if os.path.isdir(instance_path) and os.path.exists(json_path):
                with open(json_path, "r", encoding="utf-8") as f:
                    instances.append(json.load(f))
        return instances

    def create_instance(self, name, version, loader_type="Vanilla", loader_version=""):
        # Очищуємо назву від небезпечних символів для папки
        safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '_', '-')).rstrip()
        if not safe_name:
            raise ValueError("Назва інстансу не може бути порожньою")

        instance_path = os.path.join(INSTANCES_DIR, safe_name)
        if os.path.exists(instance_path):
            raise FileExistsError(f"Інстанс з назвою '{safe_name}' вже існує")

        os.makedirs(instance_path)
        
        # Створюємо стандартні підпапки для модів та збережень
        os.makedirs(os.path.join(instance_path, "mods"), exist_ok=True)
        os.makedirs(os.path.join(instance_path, "saves"), exist_ok=True)

        instance_data = {
            "name": safe_name,
            "version": version,
            "loader_type": loader_type, # Vanilla, Forge, Fabric
            "loader_version": loader_version,
            "path": instance_path
        }

        json_path = os.path.join(instance_path, "instance.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(instance_data, f, indent=4)

        return instance_data

    def delete_instance(self, name):
        instance_path = os.path.join(INSTANCES_DIR, name)
        if os.path.exists(instance_path):
            shutil.rmtree(instance_path)
            return True
        return False

    def get_instance_path(self, name):
        return os.path.join(INSTANCES_DIR, name)