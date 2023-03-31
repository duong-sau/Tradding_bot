from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, QTimer
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QDesktopWidget

from Common.common import MCN, MCNT, MNT, DISTANCE, NORMAL, ulFIBONACCI, dlFIBONACCI, \
    usFIBONACCI, dsFIBONACCI, uaFIBONACCI
from Common.m_common import m_math_dict
from Common.n_common import n_math_dict
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

        self.timer = QTimer()
        self.timer.timeout.connect(self.timer_run)
        self.timer.start(1000)

        self.input_view = InputView()
        self.m_textbox = self.input_view.m_textbox
        self.m_allocator = self.input_view.m_allocator
        self.n_textbox = self.input_view.n_textbox
        self.n_allocator = self.input_view.n_allocator
        self.min_textbox = self.input_view.min_textbox
        self.max_textbox = self.input_view.max_textbox

        self.combobox_view = ComboboxView()
        self.m_combobox = self.combobox_view.probability_box
        self.tx_long = self.combobox_view.long_radio

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
        screen_rect = desktop.screenGeometry()
        self.setGeometry(0, 0, screen_rect.width(), screen_rect.height() - 50)
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

    def timer_run(self):
        self.pnl_cal()

    def pnl_cal(self):
        M = self.m_textbox.get_value()
        ms = self.calculator_m()
        ns = self.calculator_n()
        SL = self.stop_loss_textbox.get_value()
        TP1 = self.take_profit1_textbox.get_value()
        a = self.a.get_value() / 100
        TP2 = self.take_profit2_textbox.get_value()
        X = self.margin_textbox.get_value()
        try:

            E = sum(x * y for x, y in zip(ms, ns)) / sum(ms)

            long = E - (E / X)
            short = E + (E / X)
            rx = (M * 0.1) / abs(SL - E)
            sl = M * abs(SL - E) * X / E
            tp1 = M * a * abs(TP1 - E) * X / E
            tp2 = M * (1 - a) * abs(TP2 - E) * X / E
            self.pnl_view.set_text(long, short, rx, sl, tp1, tp2)
        except:
            self.pnl_view.log_cant_cal()

    def get_value(self):
        data = {
            'm_list': self.calculator_m(),
            'n_list': self.calculator_n(),
            'min': self.min_textbox.get_value(),
            'max': self.max_textbox.get_value(),
            'sl': self.stop_loss_textbox.get_value(),
            'tp1': self.take_profit1_textbox.get_value(),
            'a': self.a.get_value() / 100,
            'tp2': self.take_profit2_textbox.get_value(),
            'b': self.b.get_value() / 100,
            'symbol': self.symbol_select.currentText(),
            'margin': self.margin_textbox.get_value()
        }
        return data

    def calculator_m(self):
        m_probability = self.get_m_probability()
        m = self.m_textbox.get_value()
        n = self.n_textbox.get_value()
        mc = self.m_allocator.get_value()
        if mc:
            m_list = mc + m_math_dict[m_probability](mc[-1], m, n - len(mc) + 1)[1:]
        else:
            m_list = m_math_dict[m_probability](0, m, n)
        return m_list

    def calculator_n(self):
        n = self.n_textbox.get_value()
        nc = self.n_allocator.get_value()
        min_val = self.min_textbox.get_value()
        max_val = self.max_textbox.get_value()
        n_probability = self.get_n_probability()

        if nc:
            n_list = nc + n_math_dict[n_probability](nc[-1], max_val, n - len(nc) + 1)[1:]
        else:
            n_list = n_math_dict[n_probability](min_val, max_val, n)
        return n_list

    def get_n_probability(self):
        probability = self.m_combobox.currentText()
        long = self.tx_long.isChecked()
        if long:

            if probability == MCN:
                m_probability = DISTANCE
            elif probability == MCNT:
                m_probability = ulFIBONACCI
            elif probability == MNT:
                m_probability = dlFIBONACCI
            else:
                m_probability = ""
        else:

            if probability == MCN:
                m_probability = DISTANCE
            elif probability == MCNT:
                m_probability = usFIBONACCI
            elif probability == MNT:
                m_probability = dsFIBONACCI
            else:
                m_probability = ""
        return m_probability

    def get_m_probability(self):
        probability = self.m_combobox.currentText()
        if probability == MCN:
            m_probability = uaFIBONACCI
        elif probability == MCNT:
            m_probability = uaFIBONACCI
        elif probability == MNT:
            m_probability = NORMAL
        else:
            m_probability = ""
        return m_probability

    @QtCore.pyqtSlot(float)
    def update_pnl(self, pnl):
        self.pnl_view.update_pnl(pnl)

    def test(self):
        try:
            self.m_textbox.textbox.setText("8000")
            self.n_textbox.textbox.setText('5')
            current_price = float(self.price_label.text())
            self.min_textbox.textbox.setText(str(current_price - 100))
            # self.min_textbox.textbox.setText(str(1800))

            self.max_textbox.textbox.setText(str(current_price + 100))
            # self.max_textbox.textbox.setText(str(2300))
            self.a.textbox.setText('25')
            self.stop_loss_textbox.textbox.setText(str(current_price - 200))
            self.take_profit1_textbox.textbox.setText(str(current_price + 200))
            self.take_profit2_textbox.textbox.setText(str(current_price + 300))
            self.margin_textbox.textbox.setText('5')
        except:
            pass
