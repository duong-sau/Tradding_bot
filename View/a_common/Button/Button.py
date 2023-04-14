from PyQt5.QtWidgets import QPushButton


class Button(QPushButton):
    def __init__(self, title, color, parent=None):
        super().__init__(parent)
        self.setText(title)
        self.color = color
        self.setStyleSheet(f"background-color: {color}; font-size: 24px")

    def disable(self):
        self.setEnabled(False)
        self.setStyleSheet(f"background-color: #000000; font-size: 24px")

    def enable(self):
        self.setEnabled(True)
        self.setStyleSheet(f"background-color: {self.color}; font-size: 24px")