# ui/add_instance_dialog.py
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, 
    QComboBox, QRadioButton, QButtonGroup, QPushButton, 
    QHBoxLayout, QLabel, QMessageBox
)
from PySide6.QtCore import Qt
from core.minecraft_runner import MinecraftRunner

class AddInstanceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Створити новий інстанс")
        self.setFixedSize(450, 300)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint) # Прибираємо знак питання
        
        self.selected_data = None # Тут зберігатиметься результат

        self.init_ui()
        self.load_versions()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Назва
        form_layout = QFormLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Мій крутий інстанс")
        form_layout.addRow("Назва інстансу:", self.name_input)

        # Версія Minecraft
        self.version_combo = QComboBox()
        self.version_combo.addItem("Завантаження версій...")
        self.version_combo.setEnabled(False)
        form_layout.addRow("Версія Minecraft:", self.version_combo)

        # Тип завантажувача
        loader_label = QLabel("Тип завантажувача:")
        self.loader_group = QButtonGroup(self)
        
        radio_layout = QHBoxLayout()
        
        self.vanilla_radio = QRadioButton("Vanilla")
        self.forge_radio = QRadioButton("Forge")
        self.fabric_radio = QRadioButton("Fabric")
        
        self.vanilla_radio.setChecked(True) # За замовчуванням Vanilla
        
        self.loader_group.addButton(self.vanilla_radio, 0)
        self.loader_group.addButton(self.forge_radio, 1)
        self.loader_group.addButton(self.fabric_radio, 2)
        
        radio_layout.addWidget(self.vanilla_radio)
        radio_layout.addWidget(self.forge_radio)
        radio_layout.addWidget(self.fabric_radio)
        radio_layout.addStretch()

        # Кнопки
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        self.cancel_btn = QPushButton("Скасувати")
        self.cancel_btn.clicked.connect(self.reject)
        
        self.create_btn = QPushButton("✨ Створити")
        self.create_btn.setObjectName("playButton") # Використовуємо стиль зеленої кнопки
        self.create_btn.clicked.connect(self.create_instance)

        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.create_btn)

        # Збираємо все
        layout.addLayout(form_layout)
        layout.addWidget(loader_label)
        layout.addLayout(radio_layout)
        layout.addStretch()
        layout.addLayout(btn_layout)

    def load_versions(self):
        """Завантажує список версій у фоновому режимі (або в основному потоці, бо це швидко)"""
        # Оскільки це просто запит JSON, він виконується миттєво
        versions = MinecraftRunner.get_vanilla_versions()
        self.version_combo.clear()
        if versions:
            self.version_combo.addItems(versions)
            self.version_combo.setEnabled(True)
            # Встановлюємо 1.20.4 за замовчуванням, якщо є
            index = self.version_combo.findText("1.20.4")
            if index != -1:
                self.version_combo.setCurrentIndex(index)
        else:
            self.version_combo.addItem("Помилка завантаження")

    def create_instance(self):
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Помилка", "Введіть назву інстансу!")
            return

        version = self.version_combo.currentText()
        
        # Визначаємо вибраний лоадер
        checked_id = self.loader_group.checkedId()
        loader_types = {0: "Vanilla", 1: "Forge", 2: "Fabric"}
        loader_type = loader_types.get(checked_id, "Vanilla")

        # Зберігаємо результат
        self.selected_data = {
            "name": name,
            "version": version,
            "loader_type": loader_type
        }
        
        self.accept() # Закриваємо діалог з результатом