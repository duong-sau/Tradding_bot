import time

from PyQt5.QtCore import QThread, pyqtSignal
from binance import ThreadedWebsocketManager

from Source.Binance import api_secret, api_key, testnet
from Source.Telegram.TelegramThread import log_error,  error_notification


class CSocketThread(QThread):
    order_trigger_signal = pyqtSignal(dict)

    def __init__(self, parent=None):
        super(CSocketThread, self).__init__(parent)
        self.conn_key, self.socket = None, None
        self.running = True
        self.socket = ThreadedWebsocketManager(api_secret=api_secret, api_key=api_key, testnet=testnet)
        self.socket.start()
        self.conn_key = self.socket.start_futures_user_socket(callback=self.process_message)

    def process_message(self, message):
        try:
            if message['e'] == 'ORDER_TRADE_UPDATE':
                self.order_trigger_signal.emit(message['o'])
            elif message['e'] == 'error':
                error_notification(message)
        except:
            log_error()

    def run(self) -> None:
        self.socket.join()

    def stop(self):
        self.socket.stop()
