from PyQt6.QtWidgets import QWidget, QHBoxLayout

from View._Common.TextBox.FloatTextBox import FloatTextBox


class COrderRange(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        h_box = QHBoxLayout(self)
        self.min_textbox = FloatTextBox('Min', "Min")
        self.max_textbox = FloatTextBox('Max', 'Max')
        h_box.addWidget(self.min_textbox)
        h_box.addWidget(self.max_textbox)
        self.setLayout(h_box)

    def get_value(self):
        return self.min_textbox.get_value(), self.max_textbox.get_value()
