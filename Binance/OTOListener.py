import sys

from binance.exceptions import BinanceRequestException, BinanceAPIException

from Binance.Common import get_stop_loss_form_limit, get_take_profit_form_limit
from View.a_common.MsgBox import msg_box

CANCELED = 'CANCELED'
FILL = 'FILLED'


class OTOListener:
    def __init__(self, client, destroy_call_back, parameter, stop_loss, take_profit, take_profit_2) -> None:
        print(parameter)
        self.destroy_call_back = destroy_call_back
        self.take_profit_1_order = {'clientOrderId': '-1'}
        self.take_profit_2_order = {'clientOrderId': '-1'}
        self.stop_loss_order = {'clientOrderId': '-1'}
        self.limit_order = {'clientOrderId': '-1'}
        self.client = client
        self.parameter = parameter
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.take_profit_2 = take_profit_2
        return

    def make_limit_order(self):
        try:
            self.limit_order = self.client.futures_create_order(**self.parameter)
        except(BinanceRequestException, BinanceAPIException):
            self.destroy()
            msg_box(sys.exc_info()[1])

    def destroy(self):
        self.destroy_call_back(self)
        pass

    def handle_limit(self, event):
        if event['X'] == CANCELED:
            self.destroy()
            return
        elif event['X'] == FILL:
            self.make_stop_loss_order()
            self.make_take_profit_1_order()

    def handle_take_profit_1(self, event):
        if event['X'] == CANCELED:
            self.destroy()
            return
        elif event['X'] == FILL:
            self.make_take_profit_2_order()
            self.destroy()
            return
        pass

    def handle_take_profit_2(self, event):
        if event['X'] == CANCELED:
            self.destroy()
            return
        elif event['X'] == FILL:
            self.cancel_stop_loss_order()
            self.destroy()
            return
        pass

    def handle_stop_loss(self, event):
        if event['X'] == CANCELED:
            self.destroy()
            return
        elif event['X'] == FILL:
            self.cancel_take_profit_1_order()
            self.cancel_take_profit_2_order()
            self.destroy()
            return
        pass

    def handle(self, event):
        try:
            if event['c'] == self.limit_order['clientOrderId']:
                self.handle_limit(event)
            elif event['c'] == self.stop_loss_order['clientOrderId']:
                self.handle_stop_loss(event)
            elif event['c'] == self.take_profit_1_order['clientOrderId']:
                self.handle_take_profit_1(event)
            else:
                print('pass')
        except (BinanceAPIException, BinanceRequestException):
            msg_box(sys.exc_info()[1])

    def make_stop_loss_order(self):
        parameter = get_stop_loss_form_limit(self.limit_order, self.stop_loss)
        self.stop_loss_order = self.client.futures_create_order(**parameter)

    def make_take_profit_1_order(self):
        parameter = get_take_profit_form_limit(self.limit_order, self.take_profit, 0.75)
        self.take_profit_1_order = self.client.futures_create_order(**parameter)

    def make_take_profit_2_order(self):
        parameter = get_take_profit_form_limit(self.limit_order, self.take_profit_2, 0.25)
        self.take_profit_2_order = self.client.futures_create_order(**parameter)

    def cancel_stop_loss_order(self):
        self.client.futures_cancel_order(
            symbol=self.stop_loss_order['symbol'],
            orderId=self.stop_loss_order['orderId']
        )

    def cancel_take_profit_1_order(self):
        if self.take_profit_1_order['orderId'] == '-1':
            return
        self.client.futures_cancel_order(
                symbol=self.take_profit_1_order['symbol'],
                orderId=self.take_profit_1_order['orderId']
            )

    def cancel_take_profit_2_order(self):
        if self.take_profit_2_order['orderId'] == '-1':
            return
        self.client.futures_cancel_order(
            symbol=self.take_profit_2_order['symbol'],
            orderId=self.take_profit_2_order['orderId']
        )
