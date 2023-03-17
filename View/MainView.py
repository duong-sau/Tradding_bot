from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout

from View.addvance_view import AdvanceView
from View.combobox_view import ComboboxView
from View.control_view import ControlView
from View.input_view import InputView
from View.pnl_view import PNLView
from View.symbol_view import SymbolView


class MainWindow(QMainWindow):
    open_order_signal = pyqtSignal(tuple)
    update_symbol_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        #
        #     # Widget
        #     self.order = COrder()
        #     self.budget = CBudget(self.order)
        #     self.profit_loss = CProfitLoss()
        #
        #     self.splitter = QSplitter()
        #     self.splitter.addWidget(self.budget)
        #     self.splitter.addWidget(self.order)
        #     self.splitter.addWidget(self.profit_loss)
        #     self.splitter.setSizes([200, 200, 100])
        #
        #     # controller
        #     self.g_box = QGroupBox()
        #     self.control_layout = QHBoxLayout()
        #     self.visualize = Visualize(self.update_symbol)

        #     self.control_layout.addWidget(self.visualize)
        #     self.control_layout.addWidget(self.long_button)
        #     self.control_layout.addWidget(self.short_button)
        #     self.g_box.setLayout(self.control_layout)
        self.input_view = InputView()
        self.combobox_view = ComboboxView()
        self.advance_view = AdvanceView()
        self.control_view = ControlView()
        self.pnl_view = PNLView()
        self.symbol_view = SymbolView()
        self.create_view()
        self.create_layout()
        self.setup_connections()

    def create_view(self):
        self.resize(800, 600)
        self.setWindowTitle('Trading Bot')

    def create_layout(self):
        # layout
        # layout = QVBoxLayout()
        # layout.addWidget(self.splitter)
        # layout.addWidget(self.g_box)
        layout = QGridLayout()
        layout.addWidget(self.input_view, 0, 0, 4, 2)
        layout.addWidget(self.advance_view, 5, 0, 3, 2)
        layout.addWidget(self.combobox_view, 0, 2, 4, 1)
        layout.addWidget(self.pnl_view, 5, 2, 3, 1)
        layout.addWidget(self.control_view, 8, 0, 1, 2)
        layout.addWidget(self.symbol_view, 8, 2, 1, 1)

        # main widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def setup_connections(self):
        return
        # self.long_button.clicked.connect(self.open_long)
        # self.short_button.clicked.connect(self.open_short)

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
        return
        self.visualize.update_price(price)

    @QtCore.pyqtSlot(list)
    def set_symbols(self, symbol_names):
        return
        self.visualize.set_symbols(symbol_names)

    @QtCore.pyqtSlot(str)
    def update_symbol(self, symbol):
        return
        self.update_symbol_signal.emit(symbol)

    def get_value(self):
        return self.budget.get_value(), self.order.get_value(), self.profit_loss.get_value(), self.visualize.get_value()
