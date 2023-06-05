import asyncio
import threading
import time

import timer
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import pyqtSignal, QTimer
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout
from binance import Client, AsyncClient
from binance.helpers import round_step_size

from Common.common import MCN, MCNT, MNT, DISTANCE, NORMAL, dlFIBONACCI, \
    dsFIBONACCI, uaFIBONACCI, dDISTANCE
from Common.m_common import m_math_dict
from Common.n_common import n_math_dict
from Telegram.TelegramThread import log_error
from View import testnet, symbol_list, get_tick_price, retry_view
from View.a_common.MsgBox import msg_box
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

        self.PricePrecision = 0.01
        self.QuantityPrecision = 0.001
        # self.timer = QTimer()
        # self.timer.timeout.connect(self.timer_run)
        # self.timer.start(1000)
        self.runner_timer = threading.Thread(target=self.timer_run)
        self.runner_timer.start()

        self.timer2 = QTimer()
        self.timer2.timeout.connect(self.retry)
        self.timer2.start(retry_view*1000)

        self.input_view = InputView()
        self.m_textbox = self.input_view.m_textbox
        self.n_textbox = self.input_view.n_textbox
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
        self.is_tp_sl = self.advance_view.is_tp_sl

        self.control_view = ControlView()
        self.long_button = self.control_view.long_button
        self.short_button = self.control_view.short_button

        self.pnl_view = PNLView(self.test)

        self.symbol_view = SymbolView()
        self.mark_price_label = self.symbol_view.mark_label
        self.current_price_label = self.symbol_view.current_label
        self.symbol_select = self.symbol_view.symbol_select

        self.create_view()
        self.create_layout()
        self.setup_connections()
        self.init_symbols()
        self.client = Client(testnet=testnet)

    def create_view(self):
        # desktop = QDesktopWidget()
        # screen_rect = desktop.screenGeometry()
        # self.setGeometry(0, 0, screen_rect.width(), screen_rect.height() - 50)
        self.setGeometry(680, 200, 1020, 600)
        self.setWindowTitle('Trading Bot')
        self.setWindowIcon(QtGui.QIcon('logo.ico'))

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
        self.combobox_view.button_group.buttonClicked.connect(self.check_enable_long_short)

    def check_enable_long_short(self):
        if self.tx_long.isChecked():
            self.long_button.enable()
            self.short_button.disable()
        else:
            self.long_button.disable()
            self.short_button.enable()

    def DAC_check(self):
        return True
        min_val = self.min_textbox.get_value()
        max_val = self.max_textbox.get_value()
        current_price = self.symbol_view.current_label.text()
        current_price = float(current_price)
        if min_val > max_val:
            msg_box("Min > Max")
            return False
        if min_val < current_price < max_val:
            msg_box("Min < Price < Max")
            return False
        if self.tx_long.isChecked():
            if min_val > current_price:
                msg_box("Min > Price")
                return False
        else:
            if max_val < current_price:
                msg_box("Max < Price")
                return False
        return True

    @QtCore.pyqtSlot()
    def open_long(self):
        if not self.DAC_check():
            return
        data = self.get_value(), 'LONG'
        self.open_order_signal.emit(data)

    @QtCore.pyqtSlot()
    def open_short(self):
        if not self.DAC_check():
            return
        data = self.get_value(), 'SHORT'
        self.open_order_signal.emit(data)

    def update_price(self):
        try:
            selected_symbol = self.symbol_select.currentText()
            ticker = self.client.futures_mark_price(symbol=selected_symbol)
            last_ticker = self.client.futures_symbol_ticker(symbol=selected_symbol)
            self.mark_price_label.setText(ticker['markPrice'])
            self.current_price_label.setText(last_ticker['price'])
        except:
            log_error()

    def init_symbols(self):
        self.symbol_select.addItems(symbol_list)

    @QtCore.pyqtSlot(str)
    def update_symbol(self, symbol):
        self.PricePrecision, self.QuantityPrecision = get_tick_price(symbol)
        self.update_symbol_signal.emit(symbol)

    def timer_run(self):
        time.sleep(5)
        while True:
            try:
                time.sleep(0.25)
                self.update_price()
                self.pnl_cal()
                self.update_n_max()
            except:
                log_error()


    def retry(self):
        client_temp = self.client
        self.client = Client(testnet=testnet)
        try:
            if client_temp is None:
                return
            client_temp.close_connection()
        except:
            print("close client false")

    def pnl_cal(self):
        long = self.tx_long.isChecked()
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
            if long:
                L = E - (M / X)
            else:
                L = E + (M / X)
            rx = (M * 0.1) / abs(SL - E)
            sl = X * (SL - E) * 100 / E
            tp1 = X * (TP1 - E) * 100 / E
            tp2 = X * (TP2 - E) * 100 / E
            self.pnl_view.set_text(L, rx, sl, tp1, tp2)
        except:
            pass

    def get_value(self):
        if self.is_tp_sl.isChecked():
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
        else:
            data = {
                'm_list': self.calculator_m(),
                'n_list': self.calculator_n(),
                'min': self.min_textbox.get_value(),
                'max': self.max_textbox.get_value(),
                'sl': -1,
                'tp1': -1,
                'a': self.a.get_value() / 100,
                'tp2': -1,
                'b': self.b.get_value() / 100,
                'symbol': self.symbol_select.currentText(),
                'margin': self.margin_textbox.get_value()
            }
        return data

    def calculator_m(self):
        m_probability = self.get_m_probability()
        m = self.m_textbox.get_value() * self.margin_textbox.get_value()
        n = self.n_textbox.get_value()
        m_list = m_math_dict[m_probability](0, m, n)
        return m_list

    def calculator_n(self):
        n = self.n_textbox.get_value()
        min_val = self.min_textbox.get_value()
        max_val = self.max_textbox.get_value()
        n_probability = self.get_n_probability()
        n_list = n_math_dict[n_probability](min_val, max_val, n)
        return n_list

    def get_n_probability(self):
        probability = self.m_combobox.currentText()
        long = self.tx_long.isChecked()
        if long:

            if probability == MCN:
                m_probability = dDISTANCE
            elif probability == MCNT:
                m_probability = dlFIBONACCI
            elif probability == MNT:
                m_probability = dlFIBONACCI
            else:
                m_probability = ""
        else:

            if probability == MCN:
                m_probability = DISTANCE
            elif probability == MCNT:
                m_probability = dsFIBONACCI
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

    def update_n_max(self):
        try:
            n = self.calculator_n_max()
            self.n_textbox.label.setText(f'Số lệnh (max: {n})')
        except:
            pass

    def calculator_n_max(self):

        margin = self.margin_textbox.get_value()

        m_probability = self.get_m_probability()
        m = self.m_textbox.get_value()

        n_probability = self.get_n_probability()
        min_val = self.min_textbox.get_value()
        max_val = self.max_textbox.get_value()

        for n in range(2, 50, 1):
            n_list = n_math_dict[n_probability](min_val, max_val, n)
            m_list = m_math_dict[m_probability](0, m, n)

            for m_val, n_val in zip(m_list, n_list):
                if round_step_size(margin * m_val / n_val, self.QuantityPrecision) < self.QuantityPrecision:
                    return n - 2
                if margin * m_val < 5:
                    return n - 2

    @QtCore.pyqtSlot(float, float)
    def update_pnl(self, pnl, sum_pnl):
        self.pnl_view.update_pnl(pnl, sum_pnl)


    # def test(self):
    #     try:
    #         self.m_textbox.textbox.setText("10000")
    #         self.n_textbox.textbox.setText('5')
    #         current_price = float(self.price_label.text())
    #         self.min_textbox.textbox.setText(str(current_price - 100))
    #         # self.min_textbox.textbox.setText(str(29000))
    #
    #         self.max_textbox.textbox.setText(str(current_price + 100))
    #         # self.max_textbox.textbox.setText(str(30000))
    #         self.a.textbox.setText('50')
    #         self.stop_loss_textbox.textbox.setText(str(current_price - 200))
    #         self.take_profit1_textbox.textbox.setText(str(current_price + 200))
    #         self.take_profit2_textbox.textbox.setText(str(current_price + 300))
    #         self.margin_textbox.textbox.setText('30')
    #     except:
    #         pass

    def test(self):
        try:
            self.m_textbox.textbox.setText("1000")
            self.n_textbox.textbox.setText('5')
            current_price = float(self.current_price_label.text())
            self.a.textbox.setText('40')
            self.margin_textbox.textbox.setText('1')
            if self.tx_long.isChecked():
                self.min_textbox.textbox.setText(str(current_price - 50))
                self.max_textbox.textbox.setText(str(current_price + 50))
                self.stop_loss_textbox.textbox.setText(str(current_price - 100))
                self.take_profit1_textbox.textbox.setText(str(current_price + 100))
                self.take_profit2_textbox.textbox.setText(str(current_price + 150))
            else:
                self.min_textbox.textbox.setText(str(current_price + 50))
                self.max_textbox.textbox.setText(str(current_price + 50))
                self.stop_loss_textbox.textbox.setText(str(current_price + 100))
                self.take_profit1_textbox.textbox.setText(str(current_price - 100))
                self.take_profit2_textbox.textbox.setText(str(current_price - 150))
        except:
            pass
