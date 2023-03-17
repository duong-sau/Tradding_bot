from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout

from View._Common.Allocator import Allocator
from View._Common.TextBox.FloatTextBox import FloatTextBox


class AdvanceView(QWidget):
    def __init__(self, parent=None):
        super(AdvanceView, self).__init__(parent)
        self.stop_loss_textbox = FloatTextBox('Stop loss', 'giá')
        self.take_profit1_textbox = FloatTextBox('Take profit 1', 'giá')
        self.take_profit2_textbox = FloatTextBox('Take profit 2', 'giá')
        self.create_widgets()
        self.create_connection()
        self.create_layout()

    def create_widgets(self):
        return

    def create_layout(self):
        layout = QVBoxLayout()
        layout.addWidget(self.stop_loss_textbox)
        layout.addWidget(self.take_profit1_textbox)
        layout.addWidget(self.take_profit2_textbox)
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
