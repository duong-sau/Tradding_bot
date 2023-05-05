from binance import ThreadedWebsocketManager
from binance.exceptions import BinanceAPIException, BinanceRequestException

from Binance import api_key, api_secret
from View.a_common.MsgBox import msg_box


class CSocket:
    def __init__(self, call_back, check_destroy):
        self.conn_key = None
        self.running = None
        self.socket = ThreadedWebsocketManager(api_secret=api_secret, api_key=api_key, tld='vi', testnet=True)
        self.call_back = call_back
        self.check_destroy = check_destroy
        self.retry()

    def retry(self):
        try:
            self.socket.start()
            self.conn_key = self.socket.start_futures_user_socket(callback=self.process_message)
        except(BinanceAPIException, BinanceRequestException):
            msg_box("kết nối tới binance lỗi")

    def process_message(self, message):
        if message['e'] == 'ORDER_TRADE_UPDATE':
            self.call_back(message['o'])
            if self.check_destroy():
                self.stop()

    def stop(self):
        self.socket.stop()


