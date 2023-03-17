import sys
import time

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, QThread
from binance.client import Client
from binance.exceptions import BinanceRequestException, BinanceAPIException

from Binance import api_key, api_secret
from Binance.Common import get_limit_from_parameter
from Binance.OTOListener import OTOListener
from View.a_common.MsgBox import msg_box


class CBinanceThread(QThread):
    update_price_signal = pyqtSignal(str)
    set_symbols_signal = pyqtSignal(list)

    def __init__(self):
        super(CBinanceThread, self).__init__()
        self.position_list = []
        self.running = True
        self.symbol = 'BTCUSDT'
        self.client = Client(api_key, api_secret, testnet=True)

    def run(self):
        while self.running:
            self.test_connection()
            self.update_price()
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
        symbol_names = []
        for symbol in symbols:
            symbol_name = symbol['symbol']
            symbol_names.append(symbol_name)
        self.set_symbols_signal.emit(symbol_names)

    def update_price(self):
        ticker = self.client.futures_mark_price(symbol=self.symbol)
        price = ticker['markPrice']
        self.update_price_signal.emit(price)

    def remove_position(self, position):
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
        for data in datas:
            symbol, quantity, price, stop_loss, take_profit_1, take_profit_2, margin, side = data
            parameter = get_limit_from_parameter(symbol, quantity, price, margin, side)
            position = OTOListener(self.client, self.remove_position, parameter, stop_loss, take_profit_1,
                                   take_profit_2)
            self.position_list.append(position)
            position.make_limit_order()
        msg_box("Đặt lệnh xong", "Thành công")
