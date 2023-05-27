import threading
import time
import typing
from multiprocessing import Pipe, Process, Queue

from PyQt5.QtCore import QThread, pyqtSignal, QTimer, QObject
from binance import ThreadedWebsocketManager

from Binance import api_key, api_secret, testnet, retry_socket
from Binance.Websocket import queue
from Telegram.TelegramThread import log_error, error_notification


def create_socket(name, process_queue, pipe):
    def call_back(message):
        print(f'{name}: {message}')
        process_queue.put(message)

    socket_thread = WebSocketProcess(call_back)
    pipe.recv()
    socket_thread.stop()


class CSocketThread(QThread):
    order_trigger_signal = pyqtSignal(dict)

    def __init__(self) -> None:
        super().__init__()
        thread = threading.Thread(target=self.get_data)
        thread.start()
        self.process_name = 0
        self.g_parent_conn, self.g_child_conn = None, None
        self.g_process = None

    def process_message(self, message):
        try:
            if message['e'] == 'ORDER_TRADE_UPDATE':
                self.order_trigger_signal.emit(message['o'])
            elif message['e'] == 'error':
                error_notification(message)
        except:
            log_error()

    def get_data(self):
        while True:
            data = queue.get()
            if data is None:
                break
            print("Received:", data)
            self.process_message(data)

    def run(self) -> None:
        while True:
            # start process
            print('start socket')
            local_parent, local_child = Pipe()
            process = Process(target=create_socket, args=(self.process_name, queue, local_child))
            process.start()
            self.process_name += 1

            print('run socket')
            # stop old process
            temp_process = self.g_process
            temp_parent, temp_child = self.g_parent_conn, self.g_child_conn
            if not temp_process is None:
                temp_parent.send("1")
                temp_process.terminate()
                temp_process.join()
                temp_process.close()

            # wait
            self.g_process = process
            self.g_parent_conn = local_parent
            self.g_child_conn = local_child
            for i in range(10):
                print(f'run socket {i}')
                time.sleep(retry_socket)


class WebSocketProcess(QThread):
    def __init__(self, call_back) -> None:
        super().__init__()
        self.socket = ThreadedWebsocketManager(api_secret=api_secret, api_key=api_key, testnet=testnet)
        self.socket.start()
        self.conn_key = self.socket.start_futures_user_socket(callback=call_back)

    def stop(self):
        self.socket.stop_socket(self.conn_key)
        self.socket.stop()
