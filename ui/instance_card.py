# ui/instance_card.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

class InstanceCard(QWidget):
    def __init__(self, instance_data, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 5, 10, 5)

        self.name_label = QLabel()
        self.name_label.setStyleSheet("font-size: 15px; font-weight: bold; color: #cdd6f4;")
        
        self.info_label = QLabel()
        self.info_label.setStyleSheet("font-size: 12px; color: #a6adc8;")

        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.info_label)
        
        self.update_data(instance_data)

    def update_data(self, data):
        self.name_label.setText(f"🎮 {data['name']}")
        loader = data.get("loader_type", "Vanilla")
        version = data.get("version")
        self.info_label.setText(f"{loader} • {version}")