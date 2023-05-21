import time

from PyQt5.QtCore import QThread, pyqtSignal
from binance import ThreadedWebsocketManager

from Binance import api_key, api_secret, testnet
from Telegram.TelegramThread import log_error


class CSocketThread(QThread):
    order_trigger_signal = pyqtSignal(dict)

    def __init__(self, parent=None):
        super(CSocketThread, self).__init__(parent)
        self.conn_key, self.socket = None, None
        self.running = True

    def retry(self):
        self.socket = ThreadedWebsocketManager(api_secret=api_secret, api_key=api_key, testnet=testnet)
        self.socket.start()
        self.conn_key = self.socket.start_futures_user_socket(callback=self.process_message)
        self.socket.join()

    def process_message(self, message):
        try:
            if message['e'] == 'ORDER_TRADE_UPDATE':
                self.order_trigger_signal.emit(message['o'])
        except:
            log_error()

    def run(self) -> None:
        while self.running:
            try:
                self.retry()
            except:
                log_error()
                time.sleep(5)

    def stop(self):
        self.running = False
        self.socket.stop()
