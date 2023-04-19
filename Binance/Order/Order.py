
class Order:

    def __init__(self, client, parameter) -> None:
        super().__init__()
        self.client = client
        self.id = ''
        self.client_id = parameter['newClientOrderId']
        self.parameter = parameter

    def place(self):
        try:
            client = self.client
            order = client.futures_create_order(**self.parameter)
            self.id = order['orderId']
        except:
            raise

    def cancel(self):
        client = self.client
        client.futures_cancel_order(
            symbol=self.parameter['symbol'],
            OrderId=self.id
        )

    def get_order_id(self):
        return [self.id]
