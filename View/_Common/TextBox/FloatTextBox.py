from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator

from View._Common.TextBox.TextBox import TextBox


class FloatTextBox(TextBox):
    def __init__(self, title, placeholder, parent=None):
        super(FloatTextBox, self).__init__(title, placeholder, parent)

    def set_validator(self):
        regex = QRegExp(r"([0-9]*[.])?[0-9]+")
        validator = QRegExpValidator(regex)
        self.textbox.setValidator(validator)

    def get_value(self):
        text = self.textbox.text()
        if text.strip() == "":
            text = 0
        return float(text)
