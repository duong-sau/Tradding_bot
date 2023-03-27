import sys
import time

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtWidgets import QMessageBox
from binance.client import Client
from binance.exceptions import BinanceRequestException, BinanceAPIException

from Binance import api_key, api_secret
from Binance.Common import get_limit_from_parameter
from Binance.OTOListener import OTOListener
from Logic.Log import log_fail
from View.a_common.MsgBox import msg_box


class CBinanceThread(QThread):
    update_price_signal = pyqtSignal(str)
    update_pnl_signal = pyqtSignal(float)
    set_symbols_signal = pyqtSignal(list)

    def __init__(self):
        super(CBinanceThread, self).__init__()
        self.position_list = []
        self.running = True
        self.pnl = 0
        self.symbol = 'BTCUSDT'
        self.client = Client(api_key, api_secret, testnet=True)

    def run(self):
        while self.running:
            self.test_connection()
            self.update_price()
            self.update_pnl()
            time.sleep(1)

    def stop(self):
        self.running = False

    def test_connection(self):
        try:
            self.client.ping()
        except (BinanceRequestException, BinanceAPIException):
            msg_box('Không thể kết nối đến server')
            sys.exit(0)

    def set_symbols(self):
        exchange_info = self.client.get_exchange_info()
        symbols = exchange_info['symbols']
        symbol_names = ['BTCUSDT', 'BTCBUSD']
        for symbol in symbols:
            symbol_name = symbol['symbol']
            if symbol in symbols:
                continue
            symbol_names.append(symbol_name)
        self.set_symbols_signal.emit(symbol_names)

    def update_price(self):
        ticker = self.client.futures_mark_price(symbol=self.symbol)
        price = ticker['markPrice']
        self.update_price_signal.emit(price)

    def update_pnl(self):
        pnl = 0
        for pos in self.position_list:
            pnl = pos.pnl + pnl
        self.update_pnl_signal.emit(self.pnl + pnl)

    def remove_position(self, position):
        self.pnl = self.pnl + position.pnl
        self.position_list.remove(position)

    @QtCore.pyqtSlot(dict)
    def handle_socket_event(self, msg):
        for position in self.position_list:
            position.handle(msg)

    @QtCore.pyqtSlot(str)
    def update_symbol(self, symbol):
        self.symbol = symbol

    @QtCore.pyqtSlot(list)
    def open_order(self, datas):
        confirm_str = ""
        for data in datas:
            symbol, quantity, price, stop_loss, take_profit_1, a, take_profit_2, b, margin, side = data
            confirm_str = confirm_str + f'Giá: {price}    |||| số lượng {quantity}\n'

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Xác nhận đặt lệnh")
        msg.setText(confirm_str)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        if msg.exec() != QMessageBox.Ok:
            return
        symbol, quantity, price, stop_loss, take_profit_1, a, take_profit_2, b, margin, side = datas[0]
        try:
            self.client.futures_change_leverage(symbol=self.symbol, leverage=int(margin))
            # margin
        except:
            log_fail("Lỗi set margin", str(sys.exc_info()[1]))

        for data in datas:
            symbol, quantity, price, stop_loss, take_profit_1, a, take_profit_2, b, margin, side = data
            parameter = get_limit_from_parameter(symbol, quantity, price, margin, side)
            position = OTOListener(self.client, self.remove_position, parameter, stop_loss, take_profit_1, a,
                                   take_profit_2, b)
            self.position_list.append(position)
            position.make_limit_order()
        msg_box("Đặt lệnh xong", "Thành công")
