from binance.exceptions import BinanceAPIException

from Binance import get_client
from Binance.Order.Order import Order


class StopMarketOrder(Order):

    def __init__(self, parameter, call_back_2021) -> None:
        super().__init__(parameter)
        self.call_back_2021 = call_back_2021

    def place(self):
        try:
            client = get_client()
            order = client.futures_create_order(**self.parameter)
            self.id = order['orderId']
        except BinanceAPIException as e:
            if e.code == -2021:
                self.call_back_2021()
