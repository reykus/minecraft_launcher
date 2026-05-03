# ui/main_window.py
import os
import sys
import subprocess
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QListWidget, QListWidgetItem, QLineEdit,
    QSlider, QMessageBox, QInputDialog, QProgressBar, QDialog
)
from PySide6.QtCore import Qt

from ui.styles import DARK_STYLE
from ui.instance_card import InstanceCard
from ui.workers import InstallWorker

from utils.settings import ConfigManager
from core.instance_manager import InstanceManager
from core.minecraft_runner import MinecraftRunner
from core.java_manager import JavaManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modern Minecraft Launcher")
        self.resize(1000, 650)
        
        # Бекенд
        self.config = ConfigManager()
        self.instances = InstanceManager()
        self.runner = MinecraftRunner()
        self.java_manager = JavaManager()
        
        self.current_instance = None
        self.worker = None # Для відстеження потоку

        self.init_ui()
        self.setStyleSheet(DARK_STYLE)
        self.load_instances_to_list()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # === ЛІВА ПАНЕЛЬ ===
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(10, 15, 10, 10)
        
        self.instance_list = QListWidget()
        self.instance_list.currentItemChanged.connect(self.on_instance_selected)
        
        self.add_instance_btn = QPushButton("➕ Додати інстанс")
        self.add_instance_btn.clicked.connect(self.add_instance_dialog)

        left_layout.addWidget(self.instance_list)
        left_layout.addWidget(self.add_instance_btn)
        left_panel.setFixedWidth(280)

        # === ПРАВА ПАНЕЛЬ ===
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(40, 30, 40, 30)

        # Інформація
        self.instance_name_label = QLabel("Оберіть інстанс")
        self.instance_name_label.setStyleSheet("font-size: 32px; font-weight: bold; color: #cdd6f4;")
        
        self.instance_info_label = QLabel("Або створіть новий")
        self.instance_info_label.setStyleSheet("font-size: 16px; color: #a6adc8;")

        # Прогрес завантаження
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False) # Ховаємо, поки не завантажуємо
        
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("font-size: 12px; color: #89b4fa; font-style: italic;")

        # Кнопки керування
        buttons_layout = QHBoxLayout()
        
        self.play_button = QPushButton("▶ ГРАТИ")
        self.play_button.setObjectName("playButton")
        self.play_button.clicked.connect(self.on_play_clicked)

        self.open_folder_btn = QPushButton("📁 Папка")
        self.open_folder_btn.clicked.connect(self.open_instance_folder)

        self.delete_button = QPushButton("🗑 Видалити")
        self.delete_button.setObjectName("deleteButton")
        self.delete_button.clicked.connect(self.delete_instance)

        buttons_layout.addWidget(self.play_button)
        buttons_layout.addWidget(self.open_folder_btn)
        buttons_layout.addWidget(self.delete_button)

        # Налаштування (Нік та RAM)
        settings_layout = QHBoxLayout()
        
        nick_layout = QVBoxLayout()
        nick_layout.addWidget(QLabel("Нікнейм:"))
        self.nick_input = QLineEdit()
        self.nick_input.setText(self.config.get("nickname"))
        self.nick_input.textChanged.connect(lambda text: self.config.set("nickname", text))
        nick_layout.addWidget(self.nick_input)

        ram_layout = QVBoxLayout()
        ram_header = QHBoxLayout()
        ram_header.addWidget(QLabel("Оперативна пам'ять (RAM):"))
        self.ram_label_value = QLabel(f"{self.config.get('ram_mb')} MB")
        self.ram_label_value.setStyleSheet("color: #89b4fa; font-weight: bold;")
        ram_header.addStretch()
        ram_header.addWidget(self.ram_label_value)
        ram_layout.addLayout(ram_header)
        
        self.ram_slider = QSlider(Qt.Horizontal)
        self.ram_slider.setMinimum(1024)
        self.ram_slider.setMaximum(16384)
        self.ram_slider.setValue(self.config.get("ram_mb"))
        self.ram_slider.valueChanged.connect(self.update_ram_label)
        ram_layout.addWidget(self.ram_slider)

        settings_layout.addLayout(nick_layout, 1)
        settings_layout.addLayout(ram_layout, 2)

        # Збираємо праву панель
        right_layout.addWidget(self.instance_name_label)
        right_layout.addWidget(self.instance_info_label)
        right_layout.addStretch()
        right_layout.addWidget(self.status_label)
        right_layout.addWidget(self.progress_bar)
        right_layout.addLayout(buttons_layout)
        right_layout.addStretch()
        right_layout.addLayout(settings_layout)

        # Головне збирання
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel)

    def load_instances_to_list(self):
        self.instance_list.clear()
        instances = self.instances.get_all_instances()
        for inst in instances:
            item = QListWidgetItem(self.instance_list)
            card = InstanceCard(inst, self.instance_list)
            item.setSizeHint(card.sizeHint())
            item.setData(Qt.UserRole, inst)
            self.instance_list.setItemWidget(item, card)

    def on_instance_selected(self, current, previous):
        if current is None:
            self.current_instance = None
            self.instance_name_label.setText("Оберіть інстанс")
            self.instance_info_label.setText("")
            return

        self.current_instance = current.data(Qt.UserRole)
        self.instance_name_label.setText(self.current_instance["name"])
        loader = self.current_instance.get("loader_type", "Vanilla")
        version = self.current_instance.get("version")
        self.instance_info_label.setText(f"Завантажувач: {loader} | Версія гри: {version}")

    def update_ram_label(self, value):
        self.ram_label_value.setText(f"{value} MB")
        self.config.set("ram_mb", value)

    def open_instance_folder(self):
        if not self.current_instance: return
        path = self.current_instance["path"]
        if sys.platform == 'win32': os.startfile(path)
        else: subprocess.Popen(['xdg-open', path])

    def delete_instance(self):
        if not self.current_instance: return
        reply = QMessageBox.question(self, "Підтвердження", 
            f"Видалити інстанс '{self.current_instance['name']}'?\nУсі моди та збереження будуть втрачені!",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.instances.delete_instance(self.current_instance["name"])
            self.load_instances_to_list()
            self.current_instance = None
            self.instance_name_label.setText("Оберіть інстанс")
            self.instance_info_label.setText("")

    def add_instance_dialog(self):
        from ui.add_instance_dialog import AddInstanceDialog
        
        dialog = AddInstanceDialog(self)
        if dialog.exec() == QDialog.Accepted and dialog.selected_data:
            data = dialog.selected_data
            try:
                self.instances.create_instance(
                    name=data["name"], 
                    version=data["version"], 
                    loader_type=data["loader_type"]
                )
                self.load_instances_to_list()
                
                # Автоматично вибираємо щойно створений інстанс
                for i in range(self.instance_list.count()):
                    item = self.instance_list.item(i)
                    if item.data(Qt.UserRole)["name"] == data["name"]:
                        self.instance_list.setCurrentItem(item)
                        break
                        
            except Exception as e:
                QMessageBox.critical(self, "Помилка", str(e))

    # === БАГАТОПОТОЧНІСТЬ ===
    
    def set_ui_busy(self, busy):
        """Блокуємо/розблокуємо кнопки під час завантаження"""
        self.play_button.setEnabled(not busy)
        self.add_instance_btn.setEnabled(not busy)
        self.delete_button.setEnabled(not busy)
        self.progress_bar.setVisible(busy)
        if not busy:
            self.progress_bar.setValue(0)

    def on_play_clicked(self):
        if not self.current_instance:
            QMessageBox.warning(self, "Увага", "Спочатку оберіть інстанс!")
            return
        
        nickname = self.nick_input.text()
        ram = self.ram_slider.value()
        mc_version = self.current_instance["version"]

        # 1. Визначаємо та завантажуємо Java (це швидко, якщо вже є)
        self.set_ui_busy(True)
        self.status_label.setText("Пошук відповідної версії Java...")
        
        required_java = self.java_manager.get_required_java_version(mc_version)
        java_path = self.java_manager.get_java_executable(required_java)

        if not java_path:
            QMessageBox.critical(self, "Помилка", "Не вдалося знайти або завантажити Java!")
            self.set_ui_busy(False)
            return

        # 2. Запускаємо фоновий потік для перевірки/завантаження файлів гри
        self.worker = InstallWorker(self.current_instance, java_path)
        self.worker.progress_signal.connect(self.progress_bar.setValue)
        self.worker.status_signal.connect(self.status_label.setText)
        self.worker.finished_signal.connect(self.on_install_finished)
        
        # Зберігаємо дані для запуску
        self._launch_data = {
            "instance": self.current_instance,
            "nickname": nickname,
            "ram": ram,
            "java_path": java_path
        }
        
        self.worker.start()

    def on_install_finished(self, success, message):
        self.set_ui_busy(False)
        self.status_label.setText(message)

        if success:
            # Перезавантажуємо дані інстансу (щоб оновився launch_version_id)
            updated_instances = self.instances.get_all_instances()
            for inst in updated_instances:
                if inst["name"] == self._launch_data["instance"]["name"]:
                    self._launch_data["instance"] = inst
                    break
            
            # Запускаємо гру!
            try:
                self.runner.launch_instance(
                    self._launch_data["instance"],
                    self._launch_data["nickname"],
                    self._launch_data["ram"],
                    self._launch_data["java_path"]
                )
            except Exception as e:
                QMessageBox.critical(self, "Помилка запуску", str(e))
        else:
            QMessageBox.critical(self, "Помилка завантаження", message)