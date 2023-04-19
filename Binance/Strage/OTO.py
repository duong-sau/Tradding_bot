import sys

from binance.exceptions import BinanceRequestException, BinanceAPIException

from Binance.Common import CANCELED, FILLED
from Binance.Order.LimitOrder import LimitOrder
from Binance.Order.StopMarketOrder import StopMarketOrder
from View.a_common.MsgBox import msg_box


class OTO:

    def __init__(self, client, limit_parameter, stop_parameter) -> None:
        super().__init__()
        self.limit_order = LimitOrder(client, limit_parameter)
        self.stop_loss_order = StopMarketOrder(client, stop_parameter)
        return

    def get_order_id(self):
        list_id = self.limit_order.get_order_id() + self.stop_loss_order.get_order_id()
        return list_id

    def place(self):
        try:
            self.limit_order.place()
        except(BinanceRequestException, BinanceAPIException):
            error = str(sys.exc_info()[1])
            return False, ""

    def handel(self, event):
        try:
            if event['i'] not in self.get_order_id():
                return
            # continue
            if event['X'] == CANCELED:
                self.destroy_handel(event)
            elif event['X'] == FILLED:
                self.fill_handle(event)
            # error

        except (BinanceAPIException, BinanceRequestException):
            msg_box(sys.exc_info()[1])

    def destroy_handel(self, event):
        pass

    def fill_handle(self, event):

        if event['i'] in self.limit_order.get_order_id():
            self.make_stop_loss()

    def make_stop_loss(self):
        try:
            self.stop_loss_order.place()
        except:
            raise
