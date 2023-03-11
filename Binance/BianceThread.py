import time

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, QThread
from binance.client import Client
from binance.exceptions import BinanceRequestException, BinanceAPIException

from Binance import api_key, api_secret
from Binance.Order import COrder


class CBinanceThread(QThread):
    update_price_signal = pyqtSignal(str)
    set_symbols_signal = pyqtSignal(list)

    def __init__(self):
        super(CBinanceThread, self).__init__()
        self.running = True
        self.client = Client(api_key, api_secret, testnet=True)

    def run(self):
        while self.running:
            self.test_connection()
            self.update_price('BTCBUSD')
            time.sleep(1)

    def stop(self):
        self.running = False

    def test_connection(self):
        try:
            self.client.ping()
        except (BinanceRequestException, BinanceAPIException):
            print("Ping failed!")

    def set_symbols(self):
        exchange_info = self.client.get_exchange_info()
        symbols = exchange_info['symbols']
        symbol_names = []
        for symbol in symbols:
            symbol_name = symbol['symbol']
            symbol_names.append(symbol_name)
        self.set_symbols_signal.emit(symbol_names)

    def update_price(self, symbol):
        ticker = self.client.get_avg_price(symbol=symbol)
        price = ticker['price']
        self.update_price_signal.emit(price)

    @QtCore.pyqtSlot(list)
    def open_order(self, datas):
        for data in datas:
            symbol, quantity, price, stop_loss, take_profit, margin, side = data
            order = COrder(self.client)
            order.open_position(symbol, side, quantity, margin)
            order.open_order(symbol, quantity, price, stop_loss, take_profit, side)
