import time

from binance import ThreadedWebsocketManager

from Binance import api_key, api_secret


def main():
    symbol = 'BNBBTC'

    twm = ThreadedWebsocketManager(api_key=api_key, api_secret=api_secret)
    # start is required to initialise its internal loop
    twm.start()

    def handle_socket_message(msg):
        print(f"message type: {msg['e']}")
        if msg['e'] == 'error':
            twm.stop()
            print('start')
        print(msg)

    twm.start_kline_socket(callback=handle_socket_message, symbol=symbol)

    # multiple sockets can be started
    twm.start_depth_socket(callback=handle_socket_message, symbol=symbol)

    # or a multiplex socket can be started like this
    # see Binance docs for stream names
    streams = ['bnbbtc@miniTicker', 'bnbbtc@bookTicker']
    twm.start_multiplex_socket(callback=handle_socket_message, streams=streams)


if __name__ == "__main__":
    try:
        main()
        while True:
            time.sleep(1)
            print('run')
    except:
        print("êcpt")
