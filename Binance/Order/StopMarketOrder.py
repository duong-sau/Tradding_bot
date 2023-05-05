from binance.exceptions import BinanceAPIException
from Binance.Order.Order import Order
from Binance.gClient import get_client


class StopMarketOrder(Order):

    def __init__(self, parameter, call_back_2021=None) -> None:
        super().__init__(parameter)
        self.call_back_2021 = call_back_2021

    def place(self):
        try:
            client = get_client()
            order = client.futures_create_order(**self.parameter)
            self.id = order['orderId']
        except BinanceAPIException as e:
            if e.code == -2021:
                print('2021')
