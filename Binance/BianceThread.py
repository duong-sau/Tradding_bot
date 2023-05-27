import sys
import time

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, QThread, QTimer
from binance.client import Client

from Binance import api_key, api_secret, testnet, retry_client
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
        self.client = Client(api_key, api_secret, testnet=testnet)
        self.controller_list = []
        self.running = True
        self.timer = QTimer()
        self.timer.timeout.connect(self.reconnect)
        self.timer.start(retry_client*1000)

    def reconnect(self):
        client_temp = self.client
        self.client = Client(api_key, api_secret, testnet=testnet)
        try:
            print('client reconnect')
            if client_temp is None:
                return
            client_temp.close_connection()
        except:
            print("close client fail")

    def run(self) -> None:
        print('Client is still running')
        time.sleep(1)

    def stop(self):
        self.running = False

    @QtCore.pyqtSlot(dict)
    def handle_socket_event(self, msg):
        try:
            order_id = msg['i']
            event = msg['X']
            price = msg['p']
            for controller in self.controller_list:
                controller.handel(self.client, order_id, event, price)
                if len(controller.position_list) == 0:
                    self.controller_list.remove(controller)
        except:
            log_error()

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
