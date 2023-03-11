from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QSplitter, QHBoxLayout, QGroupBox

from View.Budget.Budget import CBudget
from View.Order.Order import COrder
from View.ProfitLoss.CProfitLoss import CProfitLoss
from View.Style import style
from View.Visualize.Visualize import Visualize
from View._Common.Button.Button import Button


class MainWindow(QMainWindow):
    open_order_signal = pyqtSignal(tuple)

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # Widget
        self.order = COrder()
        self.budget = CBudget(self.order)
        self.profit_loss = CProfitLoss()

        self.splitter = QSplitter(Qt.Vertical)
        self.splitter.addWidget(self.budget)
        self.splitter.addWidget(self.order)
        self.splitter.addWidget(self.profit_loss)
        self.splitter.setSizes([200, 200, 100])

        # controller
        self.g_box = QGroupBox()
        self.control_layout = QHBoxLayout()
        self.visualize = Visualize()
        self.long_button = Button(" LONG ", '#00FF00')
        self.short_button = Button(" SHORT ", '#FF0000')
        self.control_layout.addWidget(self.visualize)
        self.control_layout.addWidget(self.long_button)
        self.control_layout.addWidget(self.short_button)
        self.g_box.setLayout(self.control_layout)

        self.create_view()
        self.create_layout()
        self.setStyleSheet(style)
        self.setup_connections()

    def create_view(self):
        self.resize(800, 600)
        self.setWindowTitle('Trading Bot')

    def create_layout(self):
        # layout
        layout = QVBoxLayout()
        layout.addWidget(self.splitter)
        layout.addWidget(self.g_box)

        # main widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def setup_connections(self):
        self.long_button.clicked.connect(self.open_long)
        self.short_button.clicked.connect(self.open_short)

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
        self.visualize.update_price(price)

    @QtCore.pyqtSlot(list)
    def set_symbols(self, symbol_names):
        self.visualize.set_symbols(symbol_names)

    def get_value(self):
        return self.budget.get_value(), self.order.get_value(), self.profit_loss.get_value(), self.visualize.get_value()
