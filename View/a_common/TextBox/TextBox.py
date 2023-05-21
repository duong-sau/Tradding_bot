from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QLineEdit, QHBoxLayout, QWidget, QLabel


class TextBox(QWidget):
    def __init__(self, title, placeholder, parent=None):
        super(TextBox, self).__init__(parent)
        self.label = QLabel(title)
        self.textbox = QLineEdit(self)
        self.textbox.setPlaceholderText(placeholder)

        layout = QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.textbox)
        layout.setStretchFactor(self.label, 1)
        layout.setStretchFactor(self.textbox, 2)

        self.setLayout(layout)
        self.set_validator()

    def set_validator(self):
        regex = QRegExp("[0-9,\\s]*")
        validator = QRegExpValidator(regex)
        self.textbox.setValidator(validator)
        return

    def set_string_validator(self, validator):
        regex = QRegExp(validator)
        validator = QRegExpValidator(regex)
        self.textbox.setValidator(validator)

    def get_value(self):
        text = self.textbox.text()
        if text.strip() == "":
            text = '0'
        return text

