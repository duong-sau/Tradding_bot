from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout

from View.addvance_view import AdvanceView
from View.combobox_view import ComboboxView
from View.control_view import ControlView
from View.input_view import InputView
from View.pnl_view import PNLView
from View.symbol_view import SymbolView


class MainWindow(QMainWindow):
    open_order_signal = pyqtSignal(dict)
    update_symbol_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.input_view = InputView()
        self.m_textbox = self.input_view.m_textbox
        self.n_textbox = self.input_view.n_textbox
        self.min_textbox = self.input_view.n_textbox
        self.max_textbox = self.input_view.max_textbox

        self.combobox_view = ComboboxView()
        self.m_combobox = self.combobox_view.m_combobox
        self.n_combobox = self.combobox_view.n_combobox
        self.margin_textbox = self.combobox_view.margin_input

        self.advance_view = AdvanceView()
        self.stop_loss_textbox = self.advance_view.stop_loss_textbox
        self.take_profit1_textbox = self.advance_view.take_profit1_textbox
        self.take_profit2_textbox = self.advance_view.take_profit2_textbox

        self.control_view = ControlView()
        self.long_button = self.control_view.long_button
        self.short_button = self.control_view.short_button

        self.pnl_view = PNLView()
        self.l_textbox = self.pnl_view.l_textbox
        self.r_x_textbox = self.pnl_view.r_x_textbox
        self.pnl_textbox = self.pnl_view.pnl_textbox

        self.symbol_view = SymbolView()
        self.price_label = self.symbol_view.price_label
        self.symbol_select = self.symbol_view.symbol_select

        self.create_view()
        self.create_layout()
        self.setup_connections()

    def create_view(self):
        self.resize(800, 600)
        self.setWindowTitle('Trading Bot')

    def create_layout(self):
        layout = QGridLayout()
        layout.addWidget(self.input_view, 0, 0, 4, 4)
        layout.addWidget(self.advance_view, 5, 0, 3, 4)
        layout.addWidget(self.combobox_view, 0, 4, 4, 2)
        layout.addWidget(self.pnl_view, 5, 4, 3, 2)
        layout.addWidget(self.control_view, 8, 0, 1, 4)
        layout.addWidget(self.symbol_view, 8, 4, 1, 2)

        # main widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def setup_connections(self):
        self.long_button.clicked.connect(self.open_long)
        self.short_button.clicked.connect(self.open_short)
        self.symbol_select.currentTextChanged.connect(self.update_symbol)

    @QtCore.pyqtSlot()
    def open_long(self):
        data = self.get_value(), 'BUY'
        self.open_order_signal.emit(data)

    @QtCore.pyqtSlot()
    def open_short(self):
        data = self.get_value(), 'SELL'
        self.open_order_signal.emit(data)

    @QtCore.pyqtSlot(str)
    def update_price(self, price):
        self.price_label.setText(price)

    @QtCore.pyqtSlot(list)
    def set_symbols(self, symbol_names):
        self.symbol_select.addItems(symbol_names)

    @QtCore.pyqtSlot(str)
    def update_symbol(self, symbol):
        self.update_symbol_signal.emit(symbol)

    def get_value(self):
        data = {
            'M': self.m_textbox.get_value(),
            'n': self.n_textbox.get_value(),
            'min': self.min_textbox.get_value(),
            'max': self.max_textbox.get_value(),
            'sl': self.stop_loss_textbox.get_value(),
            'tp1': self.take_profit1_textbox.get_value(),
            'tp2': self.take_profit2_textbox.get_value(),
            'm_': self.m_combobox.currentText(),
            'n_': self.n_combobox.currentText(),
            'margin': self.margin_textbox.get_value()
        }
        return data
