from PyQt5.QtWidgets import QWidget, QHBoxLayout

from View.Order.OrderRange import COrderRange
from View._Common.Allocator import Allocator
from View._Common.TextBox.IntTextBox import IntTextBox


class COrder(QWidget):
    def __init__(self, parent=None):
        super(COrder, self).__init__(parent)
        self.allocation_textbox = Allocator('Cách phân bổ', 'Nhập cách phân bổ')
        self.range_textbox = COrderRange()
        self.counter_textbox = IntTextBox('Số lệnh', 'Nhập số lệnh')

        self.create_connection()
        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        return

    def resizeEvent(self, event):
        parent_width = self.width()
        allocation_width = parent_width / 2
        range_width = parent_width / 4
        self.allocation_textbox.setFixedWidth(int(allocation_width))
        self.range_textbox.setFixedWidth(int(range_width))

    def create_layout(self):
        layout = QHBoxLayout()
        layout.addWidget(self.counter_textbox)
        layout.addWidget(self.range_textbox)
        layout.addWidget(self.allocation_textbox)
        self.setLayout(layout)

    def get_value(self):
        return self.allocation_textbox.get_value()

    def get_hint_value(self):
        order_min, order_max = self.range_textbox.get_value()
        counter = self.counter_textbox.get_value()
        return order_min, order_max, counter

    def create_connection(self):
        self.counter_textbox.textbox.textChanged.connect(
            lambda: self.allocation_textbox.update_hint_text(self.get_hint_value()))
        self.range_textbox.max_textbox.textbox.textChanged.connect(
            lambda: self.allocation_textbox.update_hint_text(self.get_hint_value()))
        self.range_textbox.min_textbox.textbox.textChanged.connect(
            lambda: self.allocation_textbox.update_hint_text(self.get_hint_value()))
        self.allocation_textbox.allocation_textbox.textbox.textChanged.connect(
            lambda: self.allocation_textbox.update_hint_text(self.get_hint_value()))
        self.allocation_textbox.allocation_select_list.currentTextChanged.connect(
            lambda: self.allocation_textbox.update_hint_text(self.get_hint_value()))