from Binance.Order.Order import Order


class StopMarketOrder(Order):

    def place(self):
        client = self.client
        order = client.futures_create_order(**self.parameter)
        self.id = order['orderId']
