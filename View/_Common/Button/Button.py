from PyQt6.QtWidgets import QPushButton


class Button(QPushButton):
    def __init__(self, title, color, parent=None):
        super().__init__(parent)
        self.setText(title)
        self.setStyleSheet(f"background-color: {color}; font-size: 24px")
