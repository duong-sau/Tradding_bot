from PyQt5.QtWidgets import QVBoxLayout, QWidget, QComboBox, QHBoxLayout

from View.Visualize.Price import PriceLabel


class Visualize(QWidget):
    def __init__(self, parent=None):
        super(Visualize, self).__init__(parent)

        # Tạo price label
        self.price_label = PriceLabel('Price')
        self.symbol_select = QComboBox()
        # Tạo layout
        layout = QHBoxLayout()
        layout.addWidget(self.price_label)
        layout.addWidget(self.symbol_select)

        # Đặt layout cho visualize widget
        self.setLayout(layout)

    def update_price(self, price):
        self.price_label.update_price(price)

    def set_symbols(self, symbol_names):
        self.symbol_select.addItems(symbol_names)

    def get_value(self):
        return self.symbol_select.currentText()