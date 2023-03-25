import time

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QLabel, QDesktopWidget

from View.addvance_view import AdvanceView
from View.combobox_view import ComboboxView
from View.control_view import ControlView
from View.input_view import InputView
from View.pnl_view import PNLView
from View.symbol_view import SymbolView
from common import math_dict


class MainWindow(QMainWindow):
    open_order_signal = pyqtSignal(tuple)
    update_symbol_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.input_view = InputView()
        self.m_textbox = self.input_view.m_textbox
        self.m_allocator = self.input_view.m_allocator
        self.n_textbox = self.input_view.n_textbox
        self.n_allocator = self.input_view.n_allocator
        self.min_textbox = self.input_view.min_textbox
        self.max_textbox = self.input_view.max_textbox

        self.combobox_view = ComboboxView()
        self.m_combobox = self.combobox_view.m_combobox
        self.n_combobox = self.combobox_view.n_combobox
        self.margin_textbox = self.combobox_view.margin_input

        self.advance_view = AdvanceView()
        self.stop_loss_textbox = self.advance_view.stop_loss_textbox
        self.stop_loss_percent = self.advance_view.stop_loss_percent
        self.take_profit1_textbox = self.advance_view.take_profit1_textbox
        self.a = self.advance_view.a
        self.take_profit1_percent = self.advance_view.take_profit1_percent
        self.take_profit2_textbox = self.advance_view.take_profit2_textbox
        self.b = self.advance_view.b
        self.take_profit2_percent = self.advance_view.take_profit2_percent

        self.control_view = ControlView()
        self.long_button = self.control_view.long_button
        self.short_button = self.control_view.short_button

        self.pnl_view = PNLView(self.test)

        self.symbol_view = SymbolView()
        self.price_label = self.symbol_view.price_label
        self.symbol_select = self.symbol_view.symbol_select

        self.create_view()
        self.create_layout()
        self.setup_connections()

    def create_view(self):
        desktop = QDesktopWidget()
        screenRect = desktop.screenGeometry()
        self.setGeometry(0, 0, screenRect.width(), screenRect.height())
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
        self.update_pnl()

    @QtCore.pyqtSlot(list)
    def set_symbols(self, symbol_names):
        self.symbol_select.addItems(symbol_names)

    @QtCore.pyqtSlot(str)
    def update_symbol(self, symbol):
        self.update_symbol_signal.emit(symbol)

    def update_pnl(self):
        M = self.m_textbox.get_value()
        n = self.n_textbox.get_value()
        mc = self.m_allocator.get_value()
        nc = self.n_allocator.get_value()
        min_val = self.min_textbox.get_value()
        max_val = self.max_textbox.get_value()
        m_ = self.m_combobox.currentText()
        n_ = self.n_combobox.currentText()
        if mc:
            ms = math_dict[m_](mc[-1], M, n - len(mc))
        else:
            ms = math_dict[m_](0, M, n)
        if nc:
            ns = math_dict[n_](nc[-1], max_val, n - len(nc))
        else:
            ns = math_dict[n_](min_val, max_val, n)
        SL = self.stop_loss_textbox.get_value()
        TP1 = self.take_profit1_textbox.get_value()
        TP2 = self.take_profit2_textbox.get_value()
        X = self.margin_textbox.get_value()
        try:

            E = sum(x * y for x, y in zip(ms, ns)) / n / sum(ns)

            long = E - (E / X)
            short = E + (E / X)
            rx = (M * 0.1) / (SL - E)
            pnl = 0
            spnl = 0
            sl = M * (SL - E) * X / E
            tp1 = M * 0.25 * (TP1 - E) * X / E
            tp2 = M * 0.25 * (TP2 - E) * X / E
            self.pnl_view.set_text(long, short, rx, pnl, spnl, sl, tp1, tp2)
        except:
            self.pnl_view.log_cant_cal()

    def get_value(self):
        data = {
            'M': self.m_textbox.get_value(),
            'n': self.n_textbox.get_value(),
            'nc': self.n_allocator.get_value(),
            'mc': self.m_allocator.get_value(),
            'min': self.min_textbox.get_value(),
            'max': self.max_textbox.get_value(),
            'sl': self.stop_loss_textbox.get_value(),
            'tp1': self.take_profit1_textbox.get_value(),
            'a': self.a.get_value(),
            'tp2': self.take_profit2_textbox.get_value(),
            'b': self.b.get_value(),
            'm_': self.m_combobox.currentText(),
            'n_': self.n_combobox.currentText(),
            'symbol': self.symbol_select.currentText(),
            'margin': self.margin_textbox.get_value()
        }
        return data

    def test(self):
        try:
            self.m_textbox.textbox.setText("800")
            self.n_textbox.textbox.setText('10')
            current_price = float(self.price_label.text())
            # self.min_textbox.textbox.setText(str(current_price - 1000))
            self.min_textbox.textbox.setText(str(1800))

            # self.max_textbox.textbox.setText(str(current_price - 1000))
            self.max_textbox.textbox.setText(str(2300))

            self.stop_loss_textbox.textbox.setText(str(current_price - 2000))
            self.take_profit1_textbox.textbox.setText(str(current_price + 2000))
            self.take_profit2_textbox.textbox.setText(str(current_price + 3000))
            self.margin_textbox.textbox.setText('5')
        except:
            pass
