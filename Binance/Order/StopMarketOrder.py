from binance.exceptions import BinanceAPIException

from Binance.Order.Order import Order


class StopMarketOrder(Order):

    def place(self):
        try:
            client = self.client
            order = client.futures_create_order(**self.parameter)
            self.id = order['orderId']
        except BinanceAPIException as e:
            print(e)
            pass
