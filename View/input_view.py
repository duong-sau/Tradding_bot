from PyQt5.QtWidgets import QWidget, QVBoxLayout

from View.a_common.HWidget import HWidget
from View.a_common.TextBox.FloatTextBox import FloatTextBox
from View.a_common.TextBox.IntTextBox import IntTextBox


class InputView(QWidget):
    def __init__(self, parent=None):
        super(InputView, self).__init__(parent)

        self.m_textbox = FloatTextBox('Số lượng tiền, đơn vị USD', 'M')
        self.n_textbox = IntTextBox('Số lệnh                         ', 'n')

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
        layout.addWidget(self.m_textbox)
        layout.addWidget(self.n_textbox)
        layout.addWidget(self.min_max_w)
        self.setLayout(layout)

    def create_connection(self):
        return
