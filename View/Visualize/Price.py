from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel


class PriceLabel(QLabel):
    def __init__(self, parent=None):
        super(PriceLabel, self).__init__(parent)

        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.setFont(font)

    def update_price(self, price):
        self.setText(str(price))
