# ui/styles.py

DARK_STYLE = """
QMainWindow {
    background-color: #1e1e2e;
}
QWidget {
    color: #cdd6f4;
    font-family: 'Segoe UI', Arial, sans-serif;
}
QListWidget {
    background-color: #181825;
    border: none;
    border-right: 2px solid #313244;
    font-size: 14px;
    outline: none;
}
QListWidget::item {
    padding: 5px;
    border-bottom: 1px solid #313244;
    border-radius: 4px;
    margin: 2px 5px;
}
QListWidget::item:selected {
    background-color: #313244;
}
QPushButton {
    background-color: transparent;
    border: 2px solid #585b70;
    border-radius: 8px;
    padding: 10px 20px;
    font-size: 14px;
    font-weight: bold;
    color: #cdd6f4;
}
QPushButton:hover {
    background-color: #313244;
    border-color: #cdd6f4;
}
QPushButton:pressed {
    background-color: #45475a;
}
QPushButton:disabled {
    background-color: transparent;
    color: #585b70;
    border-color: #313244;
}
QPushButton#playButton {
    color: #a6e3a1;
    border-color: #a6e3a1;
}
QPushButton#playButton:hover {
    background-color: #a6e3a1;
    color: #1e1e2e;
}
QPushButton#deleteButton {
    color: #f38ba8;
    border-color: #f38ba8;
}
QPushButton#deleteButton:hover {
    background-color: #f38ba8;
    color: #1e1e2e;
}
QLineEdit {
    background-color: #313244;
    border: 2px solid #45475a;
    border-radius: 6px;
    padding: 8px;
    font-size: 14px;
}
QLineEdit:focus {
    border-color: #89b4fa;
}
QSlider::groove:horizontal {
    border: 1px solid #313244;
    height: 8px;
    background: #313244;
    border-radius: 4px;
}
QSlider::handle:horizontal {
    background: #89b4fa;
    border: none;
    width: 18px;
    margin: -5px 0;
    border-radius: 9px;
}
QProgressBar {
    border: 2px solid #313244;
    border-radius: 5px;
    text-align: center;
    background-color: #181825;
    color: #cdd6f4;
    font-weight: bold;
}
QProgressBar::chunk {
    background-color: #89b4fa;
    border-radius: 3px;
}
QDialog {
    background-color: #1e1e2e;
}
QComboBox {
    background-color: #313244;
    border: 2px solid #45475a;
    border-radius: 6px;
    padding: 8px;
    font-size: 14px;
    color: #cdd6f4;
    min-height: 25px;
}
QComboBox:hover {
    border-color: #89b4fa;
}
QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: right center;
    width: 30px;
    border: none;
}
QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid #cdd6f4;
    margin-right: 10px;
}
QComboBox QAbstractItemView {
    background-color: #313244;
    border: 2px solid #45475a;
    selection-background-color: #45475a;
    outline: none;
}
QComboBox QAbstractItemView::item {
    color: #cdd6f4;
    padding: 6px;
    min-height: 25px;
}
QComboBox QAbstractItemView::item:hover {
    background-color: #45475a;
    color: #89b4fa;
}
QComboBox QAbstractItemView::item:selected {
    background-color: #45475a;
    color: #89b4fa;
}
QRadioButton {
    font-size: 14px;
    color: #cdd6f4;
    spacing: 8px;
}
QRadioButton::indicator {
    width: 16px;
    height: 16px;
    border-radius: 8px;
    border: 2px solid #45475a;
    background-color: #313244;
}
QRadioButton::indicator:checked {
    background-color: #89b4fa;
    border-color: #89b4fa;
}
QTextEdit {
    background-color: #11111b;
    color: #f38ba8;
    border: 2px solid #313244;
    border-radius: 6px;
    padding: 10px;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 13px;
}
QTextEdit:selected {
    background-color: #45475a;
    color: #cdd6f4;
}
"""