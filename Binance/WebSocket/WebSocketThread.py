import time

from PyQt5.QtCore import QThread, pyqtSignal
from binance import ThreadedWebsocketManager

from Binance import api_key, api_secret
from View.a_common.MsgBox import msg_box


class CSocketThread(QThread):
    order_trigger_signal = pyqtSignal(dict)

    def __init__(self, parent=None):
        super(CSocketThread, self).__init__(parent)
        self.conn_key = None
        self.running = None
        self.socket = ThreadedWebsocketManager(api_secret=api_secret, api_key=api_key, tld='vi', testnet=True)
        self.retry()

    def retry(self):
        try:
            self.socket.start()
            self.conn_key = self.socket.start_futures_user_socket(callback=self.process_message)
        except:
            msg_box("kết nối tới binance lỗi")

    def process_message(self, message):
        if message['e'] == 'ORDER_TRADE_UPDATE':
            self.order_trigger_signal.emit(message['o'])

    def stop(self):
        self.socket.stop()

    def run(self) -> None:
        try:
            self.socket.join()
        except:
            time.sleep(5)
            self.run()
