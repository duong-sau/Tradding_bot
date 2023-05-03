import ctypes
import sys
import time

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtWidgets import QMessageBox
from binance.client import Client
from binance.exceptions import BinanceRequestException, BinanceAPIException

from Binance import api_key, api_secret, testnet
from Binance.Common import get_limit_from_parameter
from Binance.OTOControl import OTOControl
from View.a_common.MsgBox import msg_box


class CBinanceThread(QThread):
    update_price_signal = pyqtSignal(str, str)
    set_symbols_signal = pyqtSignal(list)

    def __init__(self):
        super(CBinanceThread, self).__init__()
        self.position_list = []
        self.running = True
        self.pnl = 0
        self.current_price = 0
        self.symbol = 'BTCUSDT'
        if testnet == 'testnet':
            MessageBox = ctypes.windll.user32.MessageBoxW
            MessageBox(None, 'Chưa cài đặt testnet', 'Lỗi', 0)
            sys.exit(0)
        self.client = Client(api_key, api_secret, testnet=testnet)

    def retry(self):
        time.sleep(5)
        self.client = Client(api_key, api_secret, testnet=testnet)
        self.run()

    def run(self):
        try:
            while self.running:
                self.test_connection()
                self.update_price()
                time.sleep(0.25)
        except:
            print('retry')
            self.retry()

    def stop(self):
        self.running = False

    def test_connection(self):
        pass

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
        ticker = self.client.futures_mark_price(symbol=self.symbol)
        mark_price = ticker['markPrice']
        last_ticker = self.client.futures_symbol_ticker(symbol=self.symbol)
        self.current_price = float(last_ticker['price'])
        self.update_price_signal.emit(mark_price, last_ticker['price'])

    def remove_position(self, position):
        self.position_list.remove(position)
        del position

    @QtCore.pyqtSlot(dict)
    def handle_socket_event(self, msg):
        for position in self.position_list:
            position.handle(msg)

    @QtCore.pyqtSlot(str)
    def update_symbol(self, symbol):
        self.symbol = symbol

    @QtCore.pyqtSlot(list)
    def open_order(self, datas):
        if not self.confirm(datas):
            return
        self.change_margin(datas)
        self.make_position(datas)
        msg_box("Đặt lệnh xong", "Thành công")

    def confirm(self, datas):
        confirm_str = ""
        for data in datas:
            symbol, quantity, price, stop_loss, margin, side = data
            confirm_str = confirm_str + f'Giá: {price}    |||| số lượng {quantity}\n'
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Xác nhận đặt lệnh")
        msg.setText(confirm_str)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        if msg.exec() != QMessageBox.Ok:
            return False
        else:
            return True

    def change_margin(self, datas):
        try:
            symbol, quantity, price, stop_loss, margin, side = datas[0]
            self.client.futures_change_leverage(symbol=self.symbol, leverage=int(margin))
            # margin
        except (BinanceRequestException, BinanceAPIException):
            error = "Cài đặt margin lỗi\n" + str(sys.exc_info()[1])
            msg_box(error, "Lỗi")

    def make_position(self, datas):
        for data in datas:
            symbol, quantity, price, stop_loss, margin, side = data
            try:
                parameter = get_limit_from_parameter(symbol, quantity, price, margin, side)

                full_type = True
                if stop_loss < 0:
                    full_type = False

                position = OTOControl(self.client, self.remove_position, parameter, stop_loss, full_type)
                self.position_list.append(position)

            except:
                error_string = f"Giá: {price}  số lượng: {quantity}  x: {margin} \n"
                error = str(sys.exc_info()[1])
                error_string = error_string + error
                msg_box(error_string)
