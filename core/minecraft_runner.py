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
        version_json = os.path.join(BASE_MINECRAFT_DIR, "versions", version_id, f"{version_id}.json")
        return os.path.exists(version_json)

    @staticmethod
    def _fix_legacy_forge_folders(mc_version):
        versions_dir = os.path.join(BASE_MINECRAFT_DIR, "versions")
        if not os.path.exists(versions_dir):
            return None

        forge_folders = []
        for folder_name in os.listdir(versions_dir):
            if mc_version in folder_name and "forge" in folder_name.lower():
                forge_folders.append(folder_name)

        if len(forge_folders) > 1:
            primary_folder = None
            json_source_folder = None
            json_filename = None

            for folder in forge_folders:
                folder_path = os.path.join(versions_dir, folder)
                for item in os.listdir(folder_path):
                    if item.endswith(".jar"):
                        primary_folder = folder
                    if item.endswith(".json"):
                        json_source_folder = folder
                        json_filename = item

            if primary_folder and json_source_folder and primary_folder != json_source_folder:
                src_json = os.path.join(versions_dir, json_source_folder, json_filename)
                dst_json = os.path.join(versions_dir, primary_folder, f"{primary_folder}.json")
                
                import shutil
                shutil.move(src_json, dst_json)
                try:
                    os.rmdir(os.path.join(versions_dir, json_source_folder))
                except OSError:
                    pass
            
            return primary_folder

        elif len(forge_folders) == 1:
            return forge_folders[0]
        
        return None

    @staticmethod
    def _resolve_loader_version_id(mc_version, loader_type, loader_version_str=None):
        versions_dir = os.path.join(BASE_MINECRAFT_DIR, "versions")
        if not os.path.exists(versions_dir):
            return None

        build_id = None
        if loader_version_str:
            parts = loader_version_str.split('-')
            for part in parts:
                if part != mc_version:
                    build_id = part
                    break

        best_match = None
        for folder_name in os.listdir(versions_dir):
            if loader_type == "Forge":
                if mc_version in folder_name and "forge" in folder_name.lower():
                    if build_id and build_id in folder_name:
                        return folder_name
                    elif not build_id:
                        best_match = folder_name
            elif loader_type == "Fabric":
                if "fabric-loader" in folder_name.lower() and mc_version in folder_name:
                    return folder_name

        return best_match

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
                    version, BASE_MINECRAFT_DIR, callback=callback_dict
                )
            elif loader_type == "Forge":
                forge_version = minecraft_launcher_lib.forge.find_forge_version(version)
                minecraft_launcher_lib.forge.install_forge_version(
                    forge_version, BASE_MINECRAFT_DIR, callback=callback_dict, java=java_path
                )
                fixed_id = MinecraftRunner._fix_legacy_forge_folders(version)
                if fixed_id:
                    launch_version_id = fixed_id
                else:
                    found_id = MinecraftRunner._resolve_loader_version_id(version, "Forge", forge_version)
                    launch_version_id = found_id if found_id else f"{version}-forge-{forge_version.split('-')[-1]}"
            elif loader_type == "Fabric":
                loader_version = minecraft_launcher_lib.fabric.get_latest_loader_version()
                minecraft_launcher_lib.fabric.install_fabric(
                    version, BASE_MINECRAFT_DIR, callback=callback_dict, java=java_path
                )
                found_id = MinecraftRunner._resolve_loader_version_id(version, "Fabric")
                launch_version_id = found_id if found_id else f"fabric-loader-{loader_version}-{version}"

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
            
            kwargs = {}
            if os.name == 'nt':
                kwargs['creationflags'] = subprocess.CREATE_NO_WINDOW
            
            # ВАЖЛИВО: Не перехоплюємо stdout/stderr! javaw.exe все одно туди не пише.
            # Це дозволить грі коректно створювати вікно та лог-файли.
            process = subprocess.Popen(minecraft_command, cwd=instance_path, **kwargs)
            return process
        except Exception as e:
            print(f"Помилка генерації команди: {e}")
            return None