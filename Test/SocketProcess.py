import time

from binance import ThreadedWebsocketManager

from Binance import api_key, api_secret, testnet


class CSocket:

    def __init__(self, call_back):
        self.conn_key, self.socket = None, None
        self.socket = ThreadedWebsocketManager(api_secret=api_secret, api_key=api_key, testnet=testnet)
        self.socket.start()
        self.conn_key = self.socket.start_futures_user_socket(callback=call_back)

    def stop(self):
        self.socket.stop_socket(self.conn_key)
        self.socket.stop()


def create_socket(name, queue, pipe):
    def call_back(message):
        print(name)
        print(message)
        queue.put(message)

    socket_thread = CSocket(call_back)
    pipe.recv()
    socket_thread.stop()

