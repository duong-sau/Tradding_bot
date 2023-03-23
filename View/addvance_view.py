from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

from View.a_common.HWidget import HWidget
from View.a_common.TextBox.FloatTextBox import FloatTextBox


class AdvanceView(QWidget):
    def __init__(self, parent=None):
        super(AdvanceView, self).__init__(parent)
        self.stop_loss_textbox = FloatTextBox('Stop loss', 'giá')
        self.stop_loss_percent = QLabel("%")
        self.take_profit1_textbox = FloatTextBox('Take profit 1', 'giá')
        self.take_profit1_percent = QLabel("%")
        self.a = FloatTextBox('% tp1', 'a')
        self.take_profit2_textbox = FloatTextBox('Take profit 2', 'giá')
        self.take_profit2_percent = QLabel("%")
        self.b = FloatTextBox('% tp2', 'b')
        self.create_widgets()
        self.create_connection()
        self.create_layout()

    def create_widgets(self):
        return

    def create_layout(self):
        layout = QVBoxLayout()
        layout.addWidget(HWidget(self.stop_loss_textbox, self.stop_loss_percent))
        layout.addWidget(HWidget(self.take_profit1_textbox, self.a, self.take_profit1_percent))
        layout.addWidget(HWidget(self.take_profit2_textbox, self.b, self.take_profit2_percent))
        self.setLayout(layout)

    def get_value(self):
        return self.take_profit1_textbox.get_value()

    def get_hint_value(self):
        counter = self.order.counter_textbox.get_value()
        max_val = self.stop_loss_textbox.get_value()
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
