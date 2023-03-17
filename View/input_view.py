from PyQt5.QtWidgets import QWidget, QVBoxLayout

from View._Common.TextBox.FloatTextBox import FloatTextBox


class InputView(QWidget):
    def __init__(self, parent=None):
        super(InputView, self).__init__(parent)

        self.m_textbox = FloatTextBox('Số lượng tiền, đơn vị USD', 'M')
        self.n_textbox = FloatTextBox('Số lệnh', 'n')
        input_l = QVBoxLayout()
        input_l.addWidget(self.m_textbox)
        input_l.addWidget(self.n_textbox)
        input_w = QWidget()

        self.min_textbox = FloatTextBox('Min', 'M')
        self.max_textbox = FloatTextBox('Max', 'n')

        self.create_widgets()
        self.create_connection()
        self.create_layout()

    def create_widgets(self):
        return

    def create_layout(self):
        layout = QVBoxLayout()
        layout.addWidget(self.m_textbox)
        layout.addWidget(self.n_textbox)
        self.setLayout(layout)


    def create_connection(self):
        return
        # self.quantity_textbox.textbox.textChanged.connect(
        #     lambda: self.allocation_textbox.update_hint_text(self.get_hint_value()))
        # self.order.counter_textbox.textbox.textChanged.connect(
        #     lambda: self.allocation_textbox.update_hint_text(self.get_hint_value()))
        # self.allocation_textbox.allocation_textbox.textbox.textChanged.connect(
        #     lambda: self.allocation_textbox.update_hint_text(self.get_hint_value()))
        # self.allocation_textbox.allocation_select_list.currentTextChanged.connect(
        #     lambda: self.allocation_textbox.update_hint_text(self.get_hint_value()))
        # Connect counter_value_changed signal from Order to update_counter slot in Budget
