import sys

from binance.exceptions import BinanceRequestException, BinanceAPIException

from Binance.Common import open_limit, open_stop_loss, open_take_profit, cancel_order
from View.a_common.MsgBox import msg_box


class OTOListener:
    def __init__(self, symbol, price, margin, side, a, b, sl, tp1, tp2) -> None:
        self.client = None
        """
        PARAMETER
        """
        self.symbol = symbol
        self.price = price
        self.margin = margin
        self.side = side
        self.a = a
        self.b = b
        self.sl = sl
        self.tp1 = tp1
        self.tp2 = tp2

        """
        ORDER
        """
        self.limit_order = None
        self.sl1_order = None
        self.tp1_order = None
        self.sl2_order = None
        self.tp2_order = None
        return

    def destroy(self):
        pass

    def make_limit_order(self):
        try:
            quantity = round(self.a + self.b, 5)
            self.limit_order = open_limit(self.client, self.symbol, quantity, self.price, self.margin, self.side)
            return True
        except(BinanceRequestException, BinanceAPIException):
            error = str(sys.exc_info()[1])
            msg_box(error)
            self.destroy()
            return False

    def handel_limit(self):
        result_1 = self.make_stop_loss_1_order()
        result_2 = False
        if self.b != 0:
            result_2 = self.make_stop_loss_2_order()

        if result_1:
            self.make_take_profit_1_order()
        if result_2:
            self.make_take_profit_2_order()

    def handle_take_profit_1(self):
        self.cancel_stop_loss_1_order()
        if self.b == 0:
            self.destroy()

    def handle_take_profit_2(self):
        self.cancel_stop_loss_2_order()

    def handle_stop_loss_1(self):
        self.cancel_take_profit_1_order()
        if self.b == 0:
            self.destroy()

    def handle_stop_loss_2(self):
        self.cancel_take_profit_2_order()
        self.destroy()

    # ----------------------------------------------------------------------------------------------------
    # Create Order
    # ----------------------------------------------------------------------------------------------------
    def make_stop_loss_1_order(self):
        self.sl1_order = open_stop_loss(self.client, self.symbol, self.a, self.sl, self.side)
        return self.sl1_order

    def make_stop_loss_2_order(self):
        self.sl2_order = open_stop_loss(self.client, self.symbol, self.b, self.sl, self.side)
        return self.sl2_order

    def make_take_profit_1_order(self):
        self.tp1_order = open_take_profit(self.client, self.symbol, self.a, self.tp1, self.side)

    def make_take_profit_2_order(self):
        self.tp2_order = open_take_profit(self.client, self.symbol, self.b, self.tp2, self.side)

    # ----------------------------------------------------------------------------------------------------
    # Cancel Order
    # ----------------------------------------------------------------------------------------------------

    def cancel_stop_loss_1_order(self):
        cancel_order(self.client, self.symbol, self.sl1_order)

    def cancel_stop_loss_2_order(self):
        cancel_order(self.client, self.symbol, self.sl2_order)

    def cancel_take_profit_1_order(self):
        cancel_order(self.client, self.symbol, self.tp1_order)

    def cancel_take_profit_2_order(self):
        cancel_order(self.client, self.symbol, self.tp2_order)

    def set_client(self, client):
        self.client = client

    def get_order_ids(self):
        return [self.limit_order, self.tp1_order, self.tp2_order, self.sl1_order, self.sl2_order]
