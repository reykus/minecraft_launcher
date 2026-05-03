import os
import subprocess
import minecraft_launcher_lib
import uuid
import json

BASE_MINECRAFT_DIR = os.path.join(os.getcwd(), "data")

class MinecraftRunner:
    @staticmethod
    def get_vanilla_versions():
        try:
            versions = minecraft_launcher_lib.utils.get_version_list()
            # Фільтруємо, щоб залишити тільки офіційні релізи (без снапшотів)
            return [v["id"] for v in versions if v["type"] == "release"]
        except Exception as e:
            print(f"Помилка отримання версій: {e}")
            return []

    @staticmethod
    def install_instance(instance_data, callback_dict=None, java_path=None):
        version = instance_data["version"]
        loader_type = instance_data["loader_type"]

        print(f"Починаємо встановлення {loader_type} {version}...")

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
                print(f"Пошук актуальної версії Forge для {version}...")
                forge_version = minecraft_launcher_lib.forge.find_forge_version(version)
                print(f"Знайдено: {forge_version}")
                
                minecraft_launcher_lib.forge.install_forge_version(
                    forge_version, 
                    BASE_MINECRAFT_DIR, 
                    callback=callback_dict,
                    java=java_path
                )
                
                # Перетворюємо Maven ID на Launcher ID (1.20.4-49.2.0 -> 1.20.4-forge-49.2.0)
                launch_version_id = forge_version.replace(version, f"{version}-forge", 1)

            elif loader_type == "Fabric":
                # Отримуємо останню версію Fabric Loader
                print(f"Пошук актуальної версії Fabric Loader для {version}...")
                loader_version = minecraft_launcher_lib.fabric.get_latest_loader_version()
                print(f"Знайдено Fabric Loader: {loader_version}")
                
                # Встановлюємо Fabric (функція нічого не повертає)
                minecraft_launcher_lib.fabric.install_fabric(
                    version, 
                    BASE_MINECRAFT_DIR, 
                    callback=callback_dict,
                    java=java_path
                )
                
                # Конструюємо ID для запуску (fabric-loader-0.19.2-1.20.4)
                launch_version_id = f"fabric-loader-{loader_version}-{version}"

            # Зберігаємо точний ID для запуску
            instance_path = instance_data["path"]
            instance_data["launch_version_id"] = launch_version_id
            json_path = os.path.join(instance_path, "instance.json")
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(instance_data, f, indent=4)

            print(f"\nВстановлення успішне! ID для запуску: {launch_version_id}")
            return True
        except Exception as e:
            print(f"\nПомилка встановлення: {e}")
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
            print(f"Генерація команди запуску для {launch_version_id}...")
            minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(
                launch_version_id, BASE_MINECRAFT_DIR, options
            )
            
            print("Запуск Minecraft...")
            subprocess.Popen(minecraft_command, 
                             cwd=instance_path,
                             creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0)
            return True
        except Exception as e:
            print(f"Помилка запуску: {e}")
            return False