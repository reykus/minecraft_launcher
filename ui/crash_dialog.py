import os
import sys
import subprocess
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QTextEdit, QPushButton, QHBoxLayout, QApplication, QMessageBox
from PySide6.QtCore import Qt

class CrashReportDialog(QDialog):
    def __init__(self, error_log, instance_path="", parent=None):
        super().__init__(parent)
        self.instance_path = instance_path
        self.setWindowTitle("Помилка запуску Minecraft")
        self.resize(900, 600) 
        # ВИПРАВЛЕНО: правильна назва прапорця для приховання знака питання
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)
        
        layout = QVBoxLayout(self)

        # Заголовок
        header_layout = QHBoxLayout()
        icon_label = QLabel()
        icon_label.setText("❌")
        icon_label.setStyleSheet("font-size: 36px;")
        
        title_label = QLabel("Гра не змогла запуститися або завершилася крашем")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #f38ba8;")
        title_label.setWordWrap(True)
        
        header_layout.addWidget(icon_label)
        header_layout.addWidget(title_label, 1)
        layout.addLayout(header_layout)

        # Текстове поле з логом (велике і зручно для скролінгу)
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setPlainText(error_log)
        layout.addWidget(self.log_text, 1) # Розтягується на все вільне місце

        # Кнопки
        btn_layout = QHBoxLayout()
        
        self.open_logs_btn = QPushButton("📂 Відкрити папку логів")
        self.open_logs_btn.clicked.connect(self.open_logs_folder)
        
        btn_layout.addWidget(self.open_logs_btn)
        btn_layout.addStretch()
        
        self.copy_btn = QPushButton("📋 Копіювати лог")
        self.copy_btn.clicked.connect(self.copy_log)
        
        self.close_btn = QPushButton("Закрити")
        self.close_btn.setObjectName("deleteButton") 
        self.close_btn.clicked.connect(self.close)

        btn_layout.addWidget(self.copy_btn)
        btn_layout.addWidget(self.close_btn)
        layout.addLayout(btn_layout)

    def open_logs_folder(self):
        """Відкриває папку логів або краш-репортів"""
        target_path = self.instance_path
            
        # Якщо є папка crash-reports, відкриваємо її
        crash_path = os.path.join(self.instance_path, "crash-reports")
        if os.path.exists(crash_path):
            target_path = crash_path
        else:
            # Інакше відкриваємо папку logs
            logs_path = os.path.join(self.instance_path, "logs")
            if os.path.exists(logs_path):
                target_path = logs_path

        try:
            if sys.platform == 'win32':
                os.startfile(target_path)
            elif sys.platform == 'darwin':
                subprocess.Popen(['open', target_path])
            else:
                subprocess.Popen(['xdg-open', target_path])
        except Exception as e:
            QMessageBox.warning(self, "Помилка", f"Не вдалося відкрити папку:\n{str(e)}")

    def copy_log(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.log_text.toPlainText())
        self.copy_btn.setText("✅ Скопійовано!")