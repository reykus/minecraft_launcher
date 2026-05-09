from PySide6.QtCore import QThread, Signal
from core.minecraft_runner import MinecraftRunner
from core.java_manager import JavaManager

class InstallWorker(QThread):
    progress_signal = Signal(int)
    status_signal = Signal(str)
    finished_signal = Signal(bool, str, dict) # Додано dict для повернення оновлених даних

    def __init__(self, instance_data):
        super().__init__()
        self.instance_data = instance_data
        self._current = 0
        self._max = 0

    def run(self):
        try:
            version = self.instance_data["version"]
            loader_type = self.instance_data["loader_type"]

            # 1. Поиск и загрузка Java (теперь в фоновом потоке!)
            self.status_signal.emit(f"Пошук Java для {version}...")
            required_java = JavaManager.get_required_java_version(version)
            java_path = JavaManager.get_java_executable(required_java)

            if not java_path:
                self.finished_signal.emit(False, "Не вдалося знайти або завантажити Java!", {})
                return

            # 2. Установка Minecraft
            self.status_signal.emit(f"Встановлення {loader_type} {version}...")
            
            callbacks = {
                "setStatus": self.status_signal.emit,
                "setProgress": self._set_progress,
                "setMax": self._set_max
            }

            success = MinecraftRunner.install_instance(
                self.instance_data, 
                callback_dict=callbacks, 
                java_path=java_path
            )

            if success:
                # Оновлюємо дані інстансу (щоб отримати launch_version_id)
                from core.instance_manager import InstanceManager
                updated_instances = InstanceManager().get_all_instances()
                updated_data = next((i for i in updated_instances if i["name"] == self.instance_data["name"]), self.instance_data)
                
                self.finished_signal.emit(True, "Готово до гри!", updated_data)
            else:
                self.finished_signal.emit(False, "Помилка встановлення. Дивіться консоль.", {})
                
        except Exception as e:
            self.finished_signal.emit(False, f"Критична помилка: {str(e)}", {})

    def _set_progress(self, value):
        self._current = value
        self._calculate_percentage()

    def _set_max(self, value):
        self._max = value
        self._calculate_percentage()

    def _calculate_percentage(self):
        """Коректний підрахунок відсотків за документацією"""
        if self._max > 0:
            percentage = int((self._current / self._max) * 100)
            # Відсотки не можуть бути більше 100 (бібліотека іноді віддає криві значення наприкінці)
            percentage = min(percentage, 100) 
            self.progress_signal.emit(percentage)
        else:
            self.progress_signal.emit(0)