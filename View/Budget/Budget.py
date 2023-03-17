from PyQt6.QtWidgets import QWidget, QHBoxLayout

from View._Common.Allocator import Allocator
from View._Common.TextBox.FloatTextBox import FloatTextBox


class CBudget(QWidget):
    def __init__(self, order, parent=None):
        super(CBudget, self).__init__(parent)
        self.quantity_textbox = FloatTextBox('Số lượng tiền, đơn vị USD', 'Nhập số lượng tiền')
        self.allocation_textbox = Allocator('Cách phân bổ', 'Nhập cách phân bổ')
        self.order = order
        self.create_widgets()
        self.create_connection()
        self.create_layout()

    def create_widgets(self):
        return

    def create_layout(self):
        layout = QHBoxLayout()
        layout.addWidget(self.quantity_textbox)
        layout.addWidget(self.allocation_textbox)
        self.setLayout(layout)

    def get_value(self):
        return self.allocation_textbox.get_value()

    def get_hint_value(self):
        counter = self.order.counter_textbox.get_value()
        max_val = self.quantity_textbox.get_value()
        return 0, max_val, counter

    def create_connection(self):
        self.quantity_textbox.textbox.textChanged.connect(
            lambda: self.allocation_textbox.update_hint_text(self.get_hint_value()))
        self.order.counter_textbox.textbox.textChanged.connect(
            lambda: self.allocation_textbox.update_hint_text(self.get_hint_value()))
        self.allocation_textbox.allocation_textbox.textbox.textChanged.connect(
            lambda: self.allocation_textbox.update_hint_text(self.get_hint_value()))
        self.allocation_textbox.allocation_select_list.currentTextChanged.connect(
            lambda: self.allocation_textbox.update_hint_text(self.get_hint_value()))
        # Connect counter_value_changed signal from Order to update_counter slot in Budget
