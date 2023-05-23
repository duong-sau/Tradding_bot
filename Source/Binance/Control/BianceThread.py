import sys
import time

from PyQt5 import QtCore
from PyQt5.QtCore import QThread
from binance.client import Client

from Source.Binance import testnet, api_secret, api_key
from Source.Binance.Control.Controller import Controller
from Source.utility import MessageBox
from Source.Telegram.TelegramThread import log_error


class CBinanceThread(QThread):

    def __init__(self):
        super(CBinanceThread, self).__init__()
        self.client = Client(api_key=api_key, api_secret=api_secret, testnet=testnet)
        self.controller_list = []
        self.running = None

    def ping(self):
        print('Binance still running')

    def run(self):
        while self.running:
            try:
                self.ping()
            except:
                log_error()
                time.sleep(5)

    def stop(self):
        self.running = False

    def open_order(self, datas):
        self.set_margin(datas)
        controller = Controller()
        controller.add_position(self.client, datas)
        self.controller_list.append(controller)
        MessageBox("Đặt lệnh xong", "Thành công")

    def set_margin(self, data):
        symbol = data['symbol']
        margin = data['margin']
        try:
            self.client.futures_change_leverage(symbol=symbol, leverage=int(margin))
        except:
            log_error()
            MessageBox(sys.exc_info()[1])

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
