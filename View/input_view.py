from PyQt5.QtWidgets import QWidget, QVBoxLayout

from View._Common.HWidget import HWidget
from View._Common.TextBox.FloatTextBox import FloatTextBox
from View._Common.TextBox.IntTextBox import IntTextBox
from View._Common.VWidget import VWidget


class InputView(QWidget):
    def __init__(self, parent=None):
        super(InputView, self).__init__(parent)

        self.m_textbox = FloatTextBox('Số lượng tiền, đơn vị USD', 'M')
        self.n_textbox = IntTextBox('Số lệnh                         ', 'n')
        self.input_w = VWidget(self.m_textbox, self.n_textbox)

        self.min_textbox = FloatTextBox('Min', 'M')
        self.max_textbox = FloatTextBox('Max', 'n')
        self.min_max_w = HWidget(self.min_textbox, self.max_textbox)

        self.create_widgets()
        self.create_connection()
        self.create_layout()

    def create_widgets(self):
        return

    def create_layout(self):
        layout = QVBoxLayout()
        layout.addWidget(self.input_w)
        layout.addWidget(self.min_max_w)
        self.setLayout(layout)

    def create_connection(self):
        return
