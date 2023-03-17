from PyQt5.QtWidgets import QWidget, QHBoxLayout, QComboBox

from View.Visualize.Price import PriceLabel
from View._Common.Allocator import Allocator
from View._Common.TextBox.FloatTextBox import FloatTextBox


class SymbolView(QWidget):
    def __init__(self,  parent=None):
        super(SymbolView, self).__init__(parent)
        self.price_label = PriceLabel('Price')
        self.symbol_select = QComboBox()
        self.create_widgets()
        self.create_connection()
        self.create_layout()

    def create_widgets(self):
        return

    def create_layout(self):
        layout = QHBoxLayout()
        layout.addWidget(self.symbol_select)
        layout.addWidget(self.price_label)
        self.setLayout(layout)

    def get_value(self):
        return self.allocation_textbox.get_value()

    def get_hint_value(self):
        counter = self.order.counter_textbox.get_value()
        max_val = self.quantity_textbox.get_value()
        return 0, max_val, counter

    def create_connection(self):
        return
        # Connect counter_value_changed signal from Order to update_counter slot in Budget
