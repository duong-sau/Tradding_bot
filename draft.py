from binance.client import Client
from binance import ThreadedWebsocketManager
from binance.enums import *

from Binance import api_key, api_secret

# Khởi tạo kết nối đến Binance API
client = Client(api_key, api_secret, testnet=True)

# Đặt một lệnh bán Bitcoin với giá 10.000 USDT
symbol = 'BTCUSDT'
quantity = 0.001
price = 21000.0
# order = client.futures_create_order(
#     symbol=symbol,
#     side=SIDE_SELL,
#     type=ORDER_TYPE_LIMIT,
#     timeInForce=TIME_IN_FORCE_GTC,
#     quantity=quantity,
#     price=price)

# Đăng ký kết nối đến WebSocket API
bm = ThreadedWebsocketManager(api_secret=api_secret, api_key=api_key, testnet=True)


# Định nghĩa hàm để xử lý sự kiện khi có lệnh được khớp
def process_message(msg):
    if msg['e'] == 'executionReport' and msg['s'] == symbol:
        if msg['S'] == 'SELL' and msg['o'] == 'LIMIT' and msg['X'] == 'FILLED':
            print('Đặt lệnh bán với giá 9.500 USDT')
            # Đặt một lệnh bán Bitcoin với giá 9.500 USDT
            new_price = 22000.0
            order = client.create_order(
                symbol=symbol,
                side=SIDE_SELL,
                type=ORDER_TYPE_LIMIT,
                timeInForce=TIME_IN_FORCE_GTC,
                quantity=quantity,
                price=new_price)
        else:
            print('Không có lệnh khớp nào được tìm thấy')


# Đăng ký sự kiện khi có lệnh được khớp
conn_key = bm.start_futures_user_socket(callback=process_message)

# Bắt đầu kết nối đến WebSocket API
bm.start()

# Hủy đăng ký sự kiện khi kết thúc chương trình
bm.stop_socket(conn_key)
bm.close()
