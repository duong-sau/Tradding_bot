import re

from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator

from View._Common.TextBox.TextBox import TextBox
from common import string_to_float_list


class AllocatorTextBox(TextBox):
    def __init__(self, title, placeholder, parent=None):
        super(AllocatorTextBox, self).__init__(title, placeholder, parent)

    def set_validator(self):
        regex = QRegExp(r"((\d*\.*\d*)\,*\s*)*")
        validator = QRegExpValidator(regex)
        self.textbox.setValidator(validator)

    def get_value(self):
        text = self.textbox.text()
        if text.strip() == "":
            return []
        text = re.sub(r',\s*$', "", text)
        alc_list = text.split(',')
        alc_list = string_to_float_list(alc_list)

        return alc_list
