from PyQt5.QtWidgets import QWidget, QHBoxLayout

from View._Common.Allocator import Allocator
from View._Common.Button.Button import Button
from View._Common.TextBox.FloatTextBox import FloatTextBox


class ControlView(QWidget):
    def __init__(self, parent=None):
        super(ControlView, self).__init__(parent)
        self.long_button = Button(" LONG ", '#00FF00')
        self.short_button = Button(" SHORT ", '#FF0000')
        self.create_widgets()
        self.create_connection()
        self.create_layout()

    def create_widgets(self):
        return

    def create_layout(self):
        layout = QHBoxLayout()
        layout.addWidget(self.long_button)
        layout.addWidget(self.short_button)
        self.setLayout(layout)

    def get_value(self):
        return self.allocation_textbox.get_value()

    def get_hint_value(self):
        counter = self.order.counter_textbox.get_value()
        max_val = self.quantity_textbox.get_value()
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
