import sys

from binance import ThreadedWebsocketManager

from Source.Binance import api_secret, api_key, testnet
from Source.utility import MessageBox
from Source.Communicator.UDPClient import UpdClient


def handle_exception(exc_type, exc_value, exc_traceback):
    MessageBox(f'{exc_type}\n{exc_value}\n{exc_traceback}')


sys.excepthook = handle_exception
if __name__ == '__main__':
    communicator = UpdClient('127.0.0.2', 4565, None)


    def call_back(message):
        communicator.send_message('127.0.0.1', 4565, message)
        print(message)


    socket = ThreadedWebsocketManager(api_secret=api_secret, api_key=api_key, testnet=testnet)
    socket.start()
    socket.start_futures_user_socket(callback=call_back)
    # socket.start_kline_socket(callback=call_back, symbol='BTCUSDT')
    socket.join()
