import sys
import time

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, QThread
from binance.client import Client
from binance.exceptions import BinanceRequestException, BinanceAPIException

from Binance import api_key, api_secret, testnet, symbol_list
from Binance.Common import confirm_order
from Binance.Controller import Controller
from View.a_common.MsgBox import msg_box


class CBinanceThread(QThread):
    update_price_signal = pyqtSignal(str, str)
    update_pnl_signal = pyqtSignal(float, float)
    set_symbols_signal = pyqtSignal(list)

    def __init__(self):
        super(CBinanceThread, self).__init__()
        self.controller_list = []
        self.running = True
        self.symbol = 'BTCUSDT'
        self.client = Client(api_key, api_secret, testnet=testnet)

    def retry(self):
        time.sleep(5)
        self.client = Client(api_key, api_secret, testnet=testnet)
        self.run()

    def run(self):
        try:
            while self.running:
                self.update_price()
                time.sleep(0.25)
        except:
            print('retry')
            self.retry()

    def stop(self):
        self.running = False

    def set_symbols(self):
        exchange_info = self.client.get_exchange_info()
        # symbols = exchange_info['symbols']
        # symbol_names = ['BTCUSDT', 'BTCBUSD']
        symbol_names = symbol_list
        self.set_symbols_signal.emit(symbol_names)

    def update_price(self):
        ticker = self.client.futures_mark_price(symbol=self.symbol)
        last_ticker = self.client.futures_symbol_ticker(symbol=self.symbol)
        self.update_price_signal.emit(ticker['markPrice'], last_ticker['price'])

    @QtCore.pyqtSlot(dict)
    def handle_socket_event(self, msg):
        order_id = msg['i']
        event = msg['X']
        for controller in self.controller_list:
            controller.handel(self.client, order_id, event)
            if len(controller.position_list) == 0:
                self.controller_list.remove(controller)

    @QtCore.pyqtSlot(str)
    def update_symbol(self, symbol):
        self.symbol = symbol

    @QtCore.pyqtSlot(list)
    def open_order(self, datas):
        if not confirm_order(datas):
            return
        self.set_margin(datas)
        controller = Controller()
        controller.add_position(self.client, datas)
        self.controller_list.append(controller)
        msg_box("Đặt lệnh xong", "Thành công")

    def set_margin(self, data):
        symbol, price, margin, side, a, b, stop_loss, take_profit_1, take_profit_2 = data[0]
        try:
            self.client.futures_change_leverage(symbol=self.symbol, leverage=int(margin))
            # margin
        except(BinanceRequestException, BinanceAPIException):
            msg_box(sys.exc_info()[1])
