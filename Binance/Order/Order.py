import sys

from binance.exceptions import BinanceAPIException, BinanceRequestException

from Binance.gClient import get_client
from View.a_common.MsgBox import msg_box


class Order:

    def __init__(self, parameter) -> None:
        super().__init__()
        self.id = ''
        self.client_id = parameter['newClientOrderId']
        self.parameter = parameter

    def place(self):
        try:
            client = get_client()
            order = client.futures_create_order(**self.parameter)
            self.id = order['orderId']
        except(BinanceAPIException, BinanceRequestException):
            msg_box(sys.exc_info()[1])
            raise

    def cancel(self):
        client = get_client()
        client.futures_cancel_order(
            symbol=self.parameter['symbol'],
            orderId=self.id
        )

    def get_order_id(self):
        return [self.id]
