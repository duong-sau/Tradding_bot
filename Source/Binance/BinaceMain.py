import json
import sys
import time

from Source.Binance.Control.BianceThread import CBinanceThread
from Source.Binance.Control.WebSocketThread import CSocketThread
from Source.utility import MessageBox
from Source.Communicator.UDPClient import UPDClient


def get_startup_status():
    order_file = open('../../binance.json', mode='r')
    order = json.load(order_file)
    order_file.close()
    MessageBox(str(order))
    return order


def handle_exception(exc_type, exc_value, exc_traceback):
    MessageBox(f'{exc_type}\n{exc_value}\n{exc_traceback}')


sys.excepthook = handle_exception

if __name__ == '__main__':
    order_json = get_startup_status()

    binance_thread = CBinanceThread()
    websocket_thread = CSocketThread()
    binance_thread.start()
    websocket_thread.order_trigger_signal.connect(binance_thread.handle_socket_event)
    time.sleep(1)
    binance_thread.open_order(order_json)

    communicator = UPDClient("Binance")
    communicator.send_ping()
