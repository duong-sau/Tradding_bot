import sys
import time

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, QThread
from binance.client import Client

from Binance import api_key, api_secret, testnet
from Binance.Common import confirm_order
from Binance.Controller import Controller
from Telegram.TelegramThread import log_error
from View.a_common.MsgBox import msg_box


class CBinanceThread(QThread):
    update_price_signal = pyqtSignal(str, str)
    update_pnl_signal = pyqtSignal(float, float)
    set_symbols_signal = pyqtSignal(list)

    def __init__(self):
        super(CBinanceThread, self).__init__()
        self.client = None
        self.controller_list = []
        self.running = True

    def retry(self):
        self.client = Client(api_key, api_secret, testnet=testnet)

    def run(self):
        while self.running:
            try:
                self.retry()
                self.client.ping()
            except:
                log_error()
                time.sleep(5)

    def stop(self):
        self.running = False


    @QtCore.pyqtSlot(dict)
    def handle_socket_event(self, msg):
        try:
            order_id = msg['i']
            event = msg['X']
            for controller in self.controller_list:
                controller.handel(self.client, order_id, event)
                if len(controller.position_list) == 0:
                    self.controller_list.remove(controller)
        except:
            log_error()

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
            self.client.futures_change_leverage(symbol=symbol, leverage=int(margin))
        except:
            log_error()
            msg_box(sys.exc_info()[1])
