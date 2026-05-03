# ui/workers.py
from PySide6.QtCore import QThread, Signal
from core.minecraft_runner import MinecraftRunner
from core.java_manager import JavaManager

class InstallWorker(QThread):
    # Сигнали для оновлення UI
    progress_signal = Signal(int)      # Відсотки
    status_signal = Signal(str)        # Текст статусу
    finished_signal = Signal(bool, str) # Успіх (bool), повідомлення (str)

    def __init__(self, instance_data, java_path=None):
        super().__init__()
        self.instance_data = instance_data
        self.java_path = java_path

    def run(self):
        try:
            # Створюємо колбеки, які будуть відправляти сигнали з потоку
            callbacks = {
                "setStatus": self.status_signal.emit,
                "setProgress": self.progress_signal.emit,
                "setMax": lambda x: None
            }

            self.status_signal.emit(f"Встановлення {self.instance_data['loader_type']}...")
            success = MinecraftRunner.install_instance(
                self.instance_data, 
                callback_dict=callbacks, 
                java_path=self.java_path
            )

            if success:
                self.finished_signal.emit(True, "Готово до гри!")
            else:
                self.finished_signal.emit(False, "Помилка встановлення. Дивіться консоль.")
                
        except Exception as e:
            self.finished_signal.emit(False, f"Критична помилка: {str(e)}")