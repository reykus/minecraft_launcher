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
    background-color: #313244;
    border: none;
    border-radius: 6px;
    padding: 10px 20px;
    font-size: 14px;
    font-weight: bold;
    color: #cdd6f4;
}
QPushButton:hover {
    background-color: #45475a;
}
QPushButton:disabled {
    background-color: #181825;
    color: #585b70;
}
QPushButton#playButton {
    background-color: #a6e3a1;
    color: #1e1e2e;
    font-size: 16px;
    padding: 15px;
}
QPushButton#playButton:hover {
    background-color: #94e2d5;
}
QPushButton#deleteButton {
    background-color: #f38ba8;
    color: #1e1e2e;
}
QPushButton#deleteButton:hover {
    background-color: #eba0ac;
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
/* --- ВИПРАВЛЕННЯ ДЛЯ ВИПАДАЮЧОГО СПИСКУ --- */
QComboBox QAbstractItemView {
    background-color: #313244; /* Темний фон списку */
    border: 2px solid #45475a;
    selection-background-color: #45475a; /* Фон вибраного елемента */
    outline: none; /* Прибираємо пунктирну рамку */
}
QComboBox QAbstractItemView::item {
    color: #cdd6f4; /* Колір тексту всіх елементів */
    padding: 6px;
    min-height: 25px;
}
QComboBox QAbstractItemView::item:hover {
    background-color: #45475a; /* Фон при наведенні миші */
    color: #89b4fa; /* Світлий синій текст при наведенні */
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

"""