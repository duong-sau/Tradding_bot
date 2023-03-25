from PyQt5.QtWidgets import QWidget, QVBoxLayout

from View.a_common.HWidget import HWidget
from View.a_common.TextBox.AllocatorTextBox import AllocatorTextBox
from View.a_common.TextBox.FloatTextBox import FloatTextBox
from View.a_common.TextBox.IntTextBox import IntTextBox
from View.a_common.VWidget import VWidget


class InputView(QWidget):
    def __init__(self, parent=None):
        super(InputView, self).__init__(parent)

        self.m_textbox = FloatTextBox('Số lượng tiền, đơn vị USD', 'M')
        self.m_allocator = AllocatorTextBox('Phân bố M', 'Cách nhau bằng dấu phẩy')
        self.n_textbox = IntTextBox('Số lệnh                         ', 'n')
        self.n_allocator = AllocatorTextBox('Phân bố n', 'Cách nhau bằng dấu phẩy')
        self.input_w = VWidget(self.m_textbox, self.m_allocator, self.n_textbox, self.n_allocator)

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
