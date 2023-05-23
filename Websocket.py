import sys
import time

from Binance import api_secret, api_key, testnet
from binance import ThreadedWebsocketManager
import subprocess

from Common.UDPClient import UpdClient

on_error = True

if __name__ == '__main__':

    def retry():
        upd_client.close()
        # Chạy tệp tin a.py
        subprocess.Popen(['Websocket.exe'], shell=True)
        sys.exit(0)


    def upd_on_receive(message):
        print(message)


    upd_client = UpdClient('127.0.0.1', 4565, upd_on_receive)


    def call_back(message):
        upd_client.send_message('127.0.0.1', 4000, str(message))
        if message['e'] == "error":
            retry()

    start = False
    i = 0
    while i < 10:
        try:
            socket = ThreadedWebsocketManager(api_secret=api_secret, api_key=api_key, testnet=testnet)
            socket.start()
            # socket.start_futures_user_socket(callback=call_back)
            socket.start_kline_socket(callback=call_back, symbol='BTCUSDT')
            start = True
            break
        except:
            i += 1
            time.sleep(1)

    if start:
        upd_client.listen()
    else:
        retry()