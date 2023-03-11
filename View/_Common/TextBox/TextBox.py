from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QGroupBox, QLineEdit, QVBoxLayout


class TextBox(QGroupBox):
    def __init__(self, title, placeholder, parent=None):
        super(TextBox, self).__init__(parent)
        self.setTitle(title)
        self.textbox = QLineEdit(self)
        self.textbox.setPlaceholderText(placeholder)

        layout = QVBoxLayout()
        layout.addWidget(self.textbox)
        self.setLayout(layout)
        self.set_validator()

    def set_validator(self):
        regex = QRegExp("[0-9,\\s]*")
        validator = QRegExpValidator(regex)
        self.textbox.setValidator(validator)

    def set_string_validator(self, validator):
        regex = QRegExp(validator)
        validator = QRegExpValidator(regex)
        self.textbox.setValidator(validator)

    def get_value(self):
        text = self.textbox.text()
        if text.strip() == "":
            text = '0'
        return text
