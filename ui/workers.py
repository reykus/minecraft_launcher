import os
import time
from PySide6.QtCore import QThread, Signal
from core.minecraft_runner import MinecraftRunner
from core.java_manager import JavaManager

class InstallWorker(QThread):
    progress_signal = Signal(int)
    status_signal = Signal(str)
    finished_signal = Signal(bool, str, dict) 

    def __init__(self, instance_data):
        super().__init__()
        self.instance_data = instance_data
        self._current = 0
        self._max = 0

    def run(self):
        try:
            version = self.instance_data["version"]
            loader_type = self.instance_data["loader_type"]
            launch_version_id = self.instance_data.get("launch_version_id")

            # ==========================================
            # ВИПРАВЛЕННЯ: Спочатку шукаємо Java!
            # Без неї Forge/Fabric не зможуть встановитися.
            # ==========================================
            self.status_signal.emit("Пошук відповідної версії Java...")
            required_java = JavaManager.get_required_java_version(version)
            java_path = JavaManager.get_java_executable(required_java)

            if not java_path:
                self.finished_signal.emit(False, "Не вдалося знайти або завантажити Java! Перевірте інтернет-з'єднання.", {})
                return

            # Тепер перевіряємо, чи гра вже встановлена
            is_installed = launch_version_id and MinecraftRunner.is_version_installed(launch_version_id)

            if is_installed:
                self.status_signal.emit("Гра вже встановлена, підготовка до запуску...")
                self.progress_signal.emit(100)
            else:
                self.status_signal.emit(f"Встановлення {loader_type} {version}...")
                callbacks = {
                    "setStatus": self.status_signal.emit,
                    "setProgress": self._set_progress,
                    "setMax": self._set_max
                }
                
                # ВАЖЛИВО: Передаємо знайдений шлях до Java у функцію встановлення!
                success = MinecraftRunner.install_instance(
                    self.instance_data, 
                    callback_dict=callbacks,
                    java_path=java_path # <--- Цей параметр вирішує WinError 2
                )
                
                if not success:
                    self.finished_signal.emit(False, "Помилка встановлення. Можливо, відсутня Java або проблеми з інтернетом.", {})
                    return

            self.status_signal.emit("Запуск Minecraft...")
            self.progress_signal.emit(100)

            process = MinecraftRunner.launch_instance(
                self.instance_data,
                self.instance_data.get("_nickname", "Player"),
                self.instance_data.get("_ram", 2048),
                java_path
            )

            if not process:
                self.finished_signal.emit(False, "Не вдалося запустити процес гри.", {})
                return

            # Відстеження крашу на старті (чекаємо 12 секунд)
            self.msleep(12000) 

            exit_code = process.poll()
            
            if exit_code is not None:
                # ГРА ВПАЛА!
                error_log = f"Гра завершилася з кодом помилки {exit_code} протягом перших 12 секунд.\n\n"
                instance_path = self.instance_data["path"]
                
                crash_info = self._get_crash_log(instance_path, loader_type)
                
                error_payload = {"instance_path": instance_path}
                self.finished_signal.emit(False, error_log + crash_info, error_payload)
            else:
                # Гра працює!
                from core.instance_manager import InstanceManager
                updated_instances = InstanceManager().get_all_instances()
                updated_data = next((i for i in updated_instances if i["name"] == self.instance_data["name"]), self.instance_data)
                updated_data["_java_path"] = java_path
                self.finished_signal.emit(True, "Гра запущена успішно!", updated_data)
                
        except Exception as e:
            self.finished_signal.emit(False, f"Критична помилка лаунчера:\n{str(e)}", {})

    def _get_crash_log(self, instance_path, loader_type):
        current_time = time.time()
        
        # 1. Шукаємо свіжий crash-report
        crash_reports_dir = os.path.join(instance_path, "crash-reports")
        if os.path.exists(crash_reports_dir):
            files = os.listdir(crash_reports_dir)
            for f in files:
                if f.endswith(".txt"):
                    fpath = os.path.join(crash_reports_dir, f)
                    if current_time - os.path.getmtime(fpath) < 120:
                        with open(fpath, 'r', encoding='utf-8', errors='ignore') as file:
                            return "=== ЗНАЙДЕНО ФАЙЛ КРАШУ (crash-reports) ===\n" + file.read(30000)

        logs_dir = os.path.join(instance_path, "logs")
        
        # 2. Читаємо fml-client-latest.log для Forge
        if loader_type == "Forge":
            fml_log_path = os.path.join(logs_dir, "fml-client-latest.log")
            if os.path.exists(fml_log_path):
                with open(fml_log_path, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                    keywords = ["Exception", "Error", "FATAL", "Failed"]
                    last_index = -1
                    for kw in keywords:
                        idx = content.rfind(kw)
                        if idx > last_index:
                            last_index = idx
                    
                    if last_index != -1:
                        start = max(0, last_index - 2000)
                        return "=== ЛОГ FORGE (fml-client-latest.log) ===\n" + content[start:start+25000]
                    else:
                        return "=== ЛОГ FORGE (fml-client-latest.log) ===\n" + content[-15000:]

        # 3. Загальний лог latest.log (або для Fabric)
        latest_log_path = os.path.join(logs_dir, "latest.log")
        if os.path.exists(latest_log_path):
            with open(latest_log_path, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()
                keywords = ["Exception", "Error", "FATAL", "Stopped", "Stopping"]
                last_index = -1
                for kw in keywords:
                    idx = content.rfind(kw)
                    if idx > last_index:
                        last_index = idx
                
                if last_index != -1:
                    start = max(0, last_index - 2000)
                    return "=== ЛОГ ГРИ (latest.log) ===\n" + content[start:start+25000]
                else:
                    return "=== ЛОГ ГРИ (latest.log) ===\n" + content[-10000:]

        return "Деталі крашу не знайдено в логах."

    def _set_progress(self, value):
        self._current = value
        self._calculate_percentage()

    def _set_max(self, value):
        self._max = value
        self._calculate_percentage()

    def _calculate_percentage(self):
        if self._max > 0:
            percentage = int((self._current / self._max) * 100)
            percentage = min(percentage, 100) 
            self.progress_signal.emit(percentage)
        else:
            self.progress_signal.emit(0)