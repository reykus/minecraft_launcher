import os
import subprocess
import minecraft_launcher_lib
import uuid
import json

from utils.settings import DATA_DIR as BASE_MINECRAFT_DIR

class MinecraftRunner:
    @staticmethod
    def get_vanilla_versions():
        try:
            versions = minecraft_launcher_lib.utils.get_version_list()
            return [v["id"] for v in versions if v["type"] == "release"]
        except Exception as e:
            print(f"Помилка отримання версій: {e}")
            return []

    @staticmethod
    def is_version_installed(version_id):
        """Перевіряє, чи існує JSON файл версії на диску"""
        version_json = os.path.join(BASE_MINECRAFT_DIR, "versions", version_id, f"{version_id}.json")
        return os.path.exists(version_json)

    @staticmethod
    def install_instance(instance_data, callback_dict=None, java_path=None):
        version = instance_data["version"]
        loader_type = instance_data["loader_type"]

        if callback_dict is None:
            callback_dict = {}

        try:
            launch_version_id = version

            if loader_type == "Vanilla":
                minecraft_launcher_lib.install.install_minecraft_version(
                    version, 
                    BASE_MINECRAFT_DIR, 
                    callback=callback_dict
                )
            elif loader_type == "Forge":
                forge_version = minecraft_launcher_lib.forge.find_forge_version(version)
                minecraft_launcher_lib.forge.install_forge_version(
                    forge_version, 
                    BASE_MINECRAFT_DIR, 
                    callback=callback_dict,
                    java=java_path
                )
                launch_version_id = forge_version.replace(version, f"{version}-forge", 1)

            elif loader_type == "Fabric":
                loader_version = minecraft_launcher_lib.fabric.get_latest_loader_version()
                minecraft_launcher_lib.fabric.install_fabric(
                    version, 
                    BASE_MINECRAFT_DIR, 
                    callback=callback_dict,
                    java=java_path
                )
                launch_version_id = f"fabric-loader-{loader_version}-{version}"

            instance_path = instance_data["path"]
            instance_data["launch_version_id"] = launch_version_id
            json_path = os.path.join(instance_path, "instance.json")
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(instance_data, f, indent=4)

            return True
        except Exception as e:
            print(f"Помилка встановлення: {e}")
            return False

    @staticmethod
    def launch_instance(instance_data, nickname, ram_mb, java_path=None):
        launch_version_id = instance_data.get("launch_version_id", instance_data["version"])
        instance_path = instance_data["path"]

        offline_uuid = str(uuid.uuid3(uuid.NAMESPACE_DNS, nickname))

        options = {
            "username": nickname,
            "uuid": offline_uuid,
            "token": "",
            "jvmPath": java_path if java_path else minecraft_launcher_lib.utils.get_java_executable(),
            "ram": ram_mb,
            "gameDirectory": instance_path, 
        }

        try:
            minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(
                launch_version_id, BASE_MINECRAFT_DIR, options
            )
            
            # ВИПРАВЛЕНО: Ховаємо консоль на Windows
            kwargs = {}
            if os.name == 'nt':
                kwargs['creationflags'] = subprocess.CREATE_NO_WINDOW
            
            subprocess.Popen(minecraft_command, cwd=instance_path, **kwargs)
            return True
        except Exception as e:
            print(f"Помилка запуску: {e}")
            return False