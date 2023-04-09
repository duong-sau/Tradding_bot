from PyQt5.QtWidgets import QWidget, QHBoxLayout, QComboBox, QLabel

from View.a_common.VWidget import VWidget


class SymbolView(QWidget):
    def __init__(self, parent=None):
        super(SymbolView, self).__init__(parent)
        self.mark_label = QLabel('Price')
        self.current_label = QLabel('Price')
        self.symbol_select = QComboBox()
        self.create_layout()

    def create_layout(self):
        layout = QHBoxLayout()
        layout.addWidget(self.symbol_select)
        layout.addWidget(VWidget(self.mark_label, self.current_label))
        self.setLayout(layout)
