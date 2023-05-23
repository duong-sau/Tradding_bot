#
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator

from Source.View.a_common.TextBox.TextBox import TextBox


class IntTextBox(TextBox):
    def __init__(self, title, placeholder, parent=None):
        super(IntTextBox, self).__init__(title, placeholder, parent)

    def set_validator(self):
        regex = QRegExp(r"[0-9]*")
        validator = QRegExpValidator(regex)
        self.textbox.setValidator(validator)
        return

    def get_value(self):
        text = self.textbox.text()
        if text.strip() == "":
            text = 0
        return int(text)
