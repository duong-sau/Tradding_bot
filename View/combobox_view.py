from PyQt5.QtWidgets import QWidget, QHBoxLayout, QComboBox, QVBoxLayout

from View._Common.Allocator import Allocator
from View._Common.TextBox.FloatTextBox import FloatTextBox
from common import probability_list


class ComboboxView(QWidget):
    def __init__(self, parent=None):
        super(ComboboxView, self).__init__(parent)
        self.m_combobox = QComboBox()
        for probability in probability_list:
            self.m_combobox.addItem(probability)
        self.n_combobox = QComboBox()
        for probability in probability_list:
            self.n_combobox.addItem(probability)
        self.margin_input = FloatTextBox('Margin', '')
        self.create_widgets()
        self.create_connection()
        self.create_layout()

    def create_widgets(self):
        return

    def create_layout(self):
        layout = QVBoxLayout()
        layout.addWidget(self.m_combobox)
        layout.addWidget(self.n_combobox)
        layout.addWidget(self.margin_input)
        self.setLayout(layout)

    def get_value(self):
        return self.n_combobox.get_value()

    def get_hint_value(self):
        counter = self.order.counter_textbox.get_value()
        max_val = self.m_combobox.get_value()
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
