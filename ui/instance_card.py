from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

class InstanceCard(QWidget):
    def __init__(self, instance_data, is_installed, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 5, 10, 5)

        self.name_label = QLabel()
        self.name_label.setStyleSheet("font-size: 15px; font-weight: bold;")
        
        self.info_label = QLabel()
        self.info_label.setStyleSheet("font-size: 12px; color: #a6adc8;")

        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.info_label)
        
        self.update_data(instance_data, is_installed)

    def update_data(self, data, is_installed):
        name = data['name']
        loader = data.get("loader_type", "Vanilla")
        version = data.get("version")
        
        if is_installed:
            status_icon = "✅"
            name_color = "#a6e3a1" # Зелений
        else:
            status_icon = "⬇️"
            name_color = "#f38ba8" # Червоний

        self.name_label.setText(f"{status_icon} {name}")
        self.name_label.setStyleSheet(f"font-size: 15px; font-weight: bold; color: {name_color};")
        self.info_label.setText(f"{loader} • {version}")