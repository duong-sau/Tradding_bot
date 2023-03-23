from PyQt5.QtCore import QThread, pyqtSignal
from binance import ThreadedWebsocketManager
from binance.exceptions import BinanceAPIException, BinanceRequestException

from Binance import api_key, api_secret
from View.a_common.MsgBox import msg_box


class CSocketThread(QThread):
    order_trigger_signal = pyqtSignal(dict)

    def __init__(self, parent=None):
        super(CSocketThread, self).__init__(parent)
        self.conn_key = None
        self.running = None
        self.socket = ThreadedWebsocketManager(api_secret=api_secret, api_key=api_key, testnet=True)
        self.retry()

    def retry(self):
        try:
            self.socket.start()
            self.conn_key = self.socket.start_futures_user_socket(callback=self.process_message)
        except(BinanceAPIException, BinanceRequestException):
            msg_box("kết nối tới binance lỗi")

    def process_message(self, message):
        print(message)
        if message['e'] == 'ORDER_TRADE_UPDATE':
            self.order_trigger_signal.emit(message['o'])
        else:
            print('nothing')

    def stop(self):
        self.socket.stop()

    def run(self) -> None:
        self.socket.join()
