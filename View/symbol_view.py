from PyQt5.QtWidgets import QWidget, QHBoxLayout, QComboBox

from View.Visualize.Price import PriceLabel


class SymbolView(QWidget):
    def __init__(self, parent=None):
        super(SymbolView, self).__init__(parent)
        self.price_label = PriceLabel('Price')
        self.symbol_select = QComboBox()
        self.create_layout()

    def create_layout(self):
        layout = QHBoxLayout()
        layout.addWidget(self.symbol_select)
        layout.addWidget(self.price_label)
        self.setLayout(layout)
