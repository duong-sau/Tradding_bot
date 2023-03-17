from PyQt5.QtWidgets import QWidget, QVBoxLayout

from View._Common.TextBox.FloatTextBox import FloatTextBox


class PNLView(QWidget):
    def __init__(self, parent=None):
        super(PNLView, self).__init__(parent)
        self.l_textbox = FloatTextBox('Giá thanh lý', 'giá')
        self.r_x_textbox = FloatTextBox('Margin đề xuất', 'giá')
        self.pnl_textbox = FloatTextBox('PNL luỹ kế', 'giá')
        self.create_widgets()
        self.create_connection()
        self.create_layout()

    def create_widgets(self):
        return

    def create_layout(self):
        layout = QVBoxLayout()
        layout.addWidget(self.l_textbox)
        layout.addWidget(self.r_x_textbox)
        layout.addWidget(self.pnl_textbox)
        self.setLayout(layout)

    def get_value(self):
        return self.r_x_textbox.get_value()

    def get_hint_value(self):
        counter = self.order.counter_textbox.get_value()
        max_val = self.l_textbox.get_value()
        return 0, max_val, counter

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

