from PyQt6.QtWidgets import QLabel

from common import string_to_float_list


class AllocatorLabel(QLabel):
    def __init__(self, title, parent=None):
        super(AllocatorLabel, self).__init__(title, parent)

    def get_value(self):
        text = self.text()
        if text.strip() == "":
            text = '0'
        alc_list = text.split(',')
        alc_list = string_to_float_list(alc_list)

        return alc_list

    def set_value(self, value):
        value = str(value)[1:-1]
        self.setText(value)
