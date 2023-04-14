import sys

from binance.exceptions import BinanceAPIException, BinanceRequestException

from Binance.Common import CANCELED, FILL, get_market_from_parameter
from Binance.Order.LimitOrder import LimitOrder
from Binance.Order.StopMarketOrder import StopMarketOrder
from View.a_common.MsgBox import msg_box


class OCO:
    def __init__(self, take_profit_parameter, stop_loss_parameter) -> None:
        super().__init__()
        self.take_profit_parameter = take_profit_parameter
        self.stop_loss_parameter = stop_loss_parameter
        self.take_profit_order = StopMarketOrder(take_profit_parameter, self.make_take_profit_market)
        self.stop_loss_order = StopMarketOrder(stop_loss_parameter, self.make_stop_loss_market)

    def place(self):
        self.take_profit_order.place()
        self.stop_loss_order.place()

    def trigger_stop(self):
        self.take_profit_order.cancel()

    def trigger_take(self):
        self.stop_loss_order.cancel()

    def get_order_id(self):
        return self.take_profit_order.get_order_id() + self.stop_loss_order.get_order_id()

    def handel(self, event):
        try:
            if event['i'] not in self.get_order_id():
                return

            # continue
            if event['X'] == CANCELED:
                self.destroy_handel(event)
            elif event['X'] == FILL:
                self.fill_handle(event)
            # error

        except (BinanceAPIException, BinanceRequestException):
            msg_box(sys.exc_info()[1])

    def destroy_handel(self, event):
        pass

    def fill_handle(self, event):

        if event['i'] in self.take_profit_order.get_order_id():
            self.trigger_take()
        if event['i'] in self.stop_loss_order.get_order_id():
            self.trigger_stop()

    def make_take_profit_market(self):
        parameter = get_market_from_parameter(self.take_profit_parameter)
        order = LimitOrder(parameter)
        order.place()
        del order

    def make_stop_loss_market(self):
        self.take_profit_order.cancel()
        parameter = get_market_from_parameter(self.stop_loss_parameter)
        order = LimitOrder(parameter)
        order.place()
        del order
