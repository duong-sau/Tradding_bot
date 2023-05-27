import time

from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from binance import ThreadedWebsocketManager

from Binance import api_key, api_secret, testnet
from Telegram.TelegramThread import log_error, error_notification


class CSocketThread(QThread):
    order_trigger_signal = pyqtSignal(dict)

    def __init__(self, call_back, parent=None):
        super(CSocketThread, self).__init__(parent)
        self.conn_key, self.socket = None, None
        # self.socket = ThreadedWebsocketManager(api_secret=api_secret, api_key=api_key, testnet=testnet)
        # self.socket.start()
        # self.conn_key = self.socket.start_futures_user_socket(callback=call_back)
        self.running = True

    def process_message(self, message):
        try:
            if message['e'] == 'ORDER_TRADE_UPDATE':
                self.order_trigger_signal.emit(message['o'])
            elif message['e'] == 'error':
                error_notification(message)
        except:
            log_error()

    def run(self) -> None:
        while self.running:
            time.sleep(10)
            print('socket is running')

    def stop(self):
        self.running = False
        # self.socket.stop_socket(self.conn_key)
        # self.socket.stop()
