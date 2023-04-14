import sys

from Logic.Log import log_fail
from binance.exceptions import BinanceRequestException, BinanceAPIException

from Binance.Common import CANCELED, FILL
from Binance.Order.LimitOrder import LimitOrder
from Binance.Strage.OCO import OCO
from View.a_common.MsgBox import msg_box


class OTO:

    def __init__(self,
                 limit_parameter, take1_parameter, stop1_parameter, take2_parameter, stop2_parameter) -> None:

        super().__init__()
        self.limit_order = LimitOrder(limit_parameter)
        self.oco1 = OCO(take_profit_parameter=take1_parameter, stop_loss_parameter=stop1_parameter)
        self.oco2 = OCO(take_profit_parameter=take2_parameter, stop_loss_parameter=stop2_parameter)

        self.m = limit_parameter['quantity']
        self.e = limit_parameter['price']
        self.s = limit_parameter['symbol']

        return

    def get_order_id(self):
        list_id = self.limit_order.get_order_id() + self.oco1.get_order_id() + self.oco2.get_order_id()
        return list_id

    def place(self):
        try:
            self.limit_order.place()
        except(BinanceRequestException, BinanceAPIException):
            error = str(sys.exc_info()[1])
            log_fail("", error)
            return False, ""

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

        if event['i'] in self.limit_order.get_order_id():
            self.make_step1()
            self.make_step2()
        elif event['i'] in self.oco1.get_order_id():
            self.oco1.handel(event)
        elif event['i'] in self.oco2.get_order_id():
            self.oco2.handel(event)

    def make_step1(self):
        try:
            self.oco1.place()
        except:
            raise

    def make_step2(self):
        try:
            self.oco2.place()
        except:
            raise
