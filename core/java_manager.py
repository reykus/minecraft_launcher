import os
import sys
import json
import platform
import requests
import zipfile
import tarfile
import stat

JAVA_DIR = os.path.join(os.getcwd(), "data", "java")

class JavaManager:
    # Мапінг версій Minecraft до потрібної версії Java
    @staticmethod
    def get_required_java_version(mc_version):
        """Визначає потрібну версію Java на основі версії MC"""
        try:
            # Витягуємо цифри з версії (напр. "1.20.4" -> [1, 20, 4] або "fabric-loader-0.15-1.20.4" -> [1, 20, 4])
            parts = mc_version.split("-")
            version_str = parts[-1] if len(parts) > 1 and parts[-1][0].isdigit() else parts[0]
            major = int(version_str.split(".")[1])
            
            if major < 17:
                return 8
            elif major == 20 and len(version_str.split(".")) > 2 and int(version_str.split(".")[2]) >= 5:
                return 21 # 1.20.5 і новіше
            elif major >= 21:
                return 21
            else:
                return 17 # 1.17 - 1.20.4
        except:
            return 17 # Значення за замовчуванням

    @staticmethod
    def get_java_executable(java_version):
        """Повертає шлях до виконуваного файлу Java або завантажує його"""
        java_path = JavaManager._find_local_java(java_version)
        if java_path:
            print(f"Знайдено Java {java_version} за шляхом: {java_path}")
            return java_path

        print(f"Java {java_version} не знайдено. Починаємо завантаження...")
        return JavaManager._download_java(java_version)

    @staticmethod
    def _find_local_java(java_version):
        """Шукає завантажену Java у папці data/java/"""
        version_dir = os.path.join(JAVA_DIR, f"java-{java_version}")
        if not os.path.exists(version_dir):
            return None

        # Шукаємо виконуваний файл у підпапках
        for root, dirs, files in os.walk(version_dir):
            if sys.platform == "win32" and "javaw.exe" in files:
                return os.path.join(root, "javaw.exe")
            elif sys.platform.startswith("linux") and "java" in files:
                return os.path.join(root, "java")
        return None

    @staticmethod
    def _download_java(java_version):
        """Завантажує Adoptium (Eclipse Temurin) та розпаковує його"""
        os.makedirs(JAVA_DIR, exist_ok=True)
        
        # Визначаємо ОС та архітектуру для API Adoptium
        os_type = "windows" if sys.platform == "win32" else "linux"
        arch = "x64"
        image_type = "jdk"

        url = f"https://api.adoptium.net/v3/assets/latest/{java_version}/hotspot"
        params = {
            "architecture": arch,
            "image_type": image_type,
            "os": os_type,
            "vendor": "eclipse"
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            if not data:
                print("Не вдалося знайти реліз Java на Adoptium.")
                return None

            package = data[0]["binary"]["package"]
            download_url = package["link"]
            file_name = package["name"]

            download_path = os.path.join(JAVA_DIR, file_name)
            target_dir = os.path.join(JAVA_DIR, f"java-{java_version}")

            # Завантаження файлу з прогресом
            print(f"Завантаження {file_name}...")
            with requests.get(download_url, stream=True) as r:
                r.raise_for_status()
                with open(download_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)

            # Розпакування
            print("Розпакування...")
            if file_name.endswith(".zip"):
                with zipfile.ZipFile(download_path, 'r') as zip_ref:
                    zip_ref.extractall(target_dir)
            elif file_name.endswith(".tar.gz"):
                with tarfile.open(download_path, 'r:gz') as tar_ref:
                    tar_ref.extractall(target_dir)

            # Видаляємо архів
            os.remove(download_path)

            # Для Linux: видаємо права на виконання
            if sys.platform.startswith("linux"):
                java_exec = JavaManager._find_local_java(java_version)
                if java_exec:
                    os.chmod(java_exec, os.stat(java_exec).st_mode | stat.S_IEXEC)

            print("Java успішно встановлено!")
            return JavaManager._find_local_java(java_version)

        except Exception as e:
            print(f"Помилка завантаження Java: {e}")
            return None