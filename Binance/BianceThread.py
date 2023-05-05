import ctypes
import sys
import time

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtWidgets import QMessageBox
from binance.client import Client
from binance.exceptions import BinanceRequestException, BinanceAPIException

from Binance import api_key, api_secret, testnet
from Binance.PositionControl import PositionControl
from Binance.gClient import set_client
from View.a_common.MsgBox import msg_box


def check_testnet():
    if testnet == 'error':
        MessageBox = ctypes.windll.user32.MessageBoxW
        MessageBox(None, 'Chưa cài đặt testnet', 'Lỗi', 0)
        sys.exit(0)





class CBinanceThread(QThread):
    update_price_signal = pyqtSignal(str, str)
    update_pnl_signal = pyqtSignal(float, float)
    set_symbols_signal = pyqtSignal(list)

    def __init__(self):
        super(CBinanceThread, self).__init__()
        self.client = None
        self.position_control = PositionControl()
        self.running = True
        self.symbol = 'BTCUSDT'
        check_testnet()
        self.init_client()

    def init_client(self):
        self.client = Client(api_key, api_secret, testnet=testnet)
        set_client(self.client)

    def retry(self):
        time.sleep(1)
        self.init_client()
        self.run()

    def run(self):
        try:
            while self.running:
                self.update_price()
                time.sleep(0.25)
        except(BinanceAPIException, BinanceRequestException):
            print('Binance thread retry')
            self.retry()
        except:
            print("update price error")

    def stop(self):
        self.running = False

    def set_symbols(self):
        exchange_info = self.client.get_exchange_info()
        symbols = exchange_info['symbols']
        symbol_names = ['BTCUSDT', 'BTCBUSD']
        for symbol in symbols:
            symbol_name = symbol['symbol']
            if symbol_name in symbols:
                continue
            symbol_names.append(symbol_name)
        self.set_symbols_signal.emit(symbol_names)

    def update_price(self):
        mark_ticker = self.client.futures_mark_price(symbol=self.symbol)
        mark_price = mark_ticker['markPrice']
        last_ticker = self.client.futures_symbol_ticker(symbol=self.symbol)
        current_price = last_ticker['price']
        self.update_price_signal.emit(mark_price, current_price)

    @QtCore.pyqtSlot(dict)
    def handle_socket_event(self, event):
        self.position_control.handel(event)

    @QtCore.pyqtSlot(str)
    def update_symbol(self, symbol):
        self.symbol = symbol

    @QtCore.pyqtSlot(list)
    def open_order(self, datas):
        self.change_margin(datas)
        self.position_control.add_batch(datas)
        msg_box("Đặt lệnh xong", "Thành công")

    def change_margin(self, datas):
        symbol, quantity, price, tp, sl, margin, side = datas[0]
        try:
            self.client.futures_change_leverage(symbol=self.symbol, leverage=int(margin))
            # margin
        except (BinanceRequestException, BinanceAPIException):
            msg_box("Cài đặt margin lỗi", "Lỗi")
