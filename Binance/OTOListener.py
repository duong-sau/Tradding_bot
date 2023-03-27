import sys
from collections import OrderedDict
from binance.exceptions import BinanceRequestException, BinanceAPIException

from Binance.Common import get_stop_loss_form_limit, get_take_profit_form_limit, open_order
from Logic.Log import log_order, log_fail
from View.a_common.MsgBox import msg_box

CANCELED = 'CANCELED'
FILL = 'FILLED'


class OTOListener:
    def __init__(self, client, destroy_call_back, parameter, stop_loss, take_profit, a, take_profit_2, b) -> None:

        self.limit_order = None
        self.destroy_call_back = destroy_call_back

        self.m = parameter['quantity']
        self.e = parameter['price']
        self.s = parameter['symbol']
        self.margin = parameter['leverage']

        self.action_dict = {
            'limit': self.handle_limit,
            'stop1': self.handle_stop_loss_1,
            'stop2': self.handle_stop_loss_2,
            'take1': self.handle_take_profit_1,
            'take2': self.handle_take_profit_2
        }

        self.pnl = 0

        self.client = client
        self.parameter = parameter

        self.stop_loss = stop_loss

        self.take_profit_1 = take_profit
        self.a = a

        self.take_profit_2 = take_profit_2
        self.b = b
        return

    def destroy(self):
        self.destroy_call_back(self)
        pass

    def make_limit_order(self):
        try:
            limit_order = open_order(self.client, self.parameter)
            self.limit_order = limit_order
            limit_id = limit_order['clientOrderId']
            self.replace_key(limit_id, 'limit')

        except(BinanceRequestException, BinanceAPIException):
            self.destroy()
            log_fail(self.limit_order['clientOrderId'], sys.exc_info()[1])
            msg_box(sys.exc_info()[1])

    def handle_limit(self):
        self.make_stop_loss_1_order()
        self.make_stop_loss_2_order()

        self.make_take_profit_1_order()
        self.make_take_profit_2_order()

    def handle_take_profit_1(self):
        self.cancel_stop_loss_1_order()
        self.update_pnl(self.take_profit_1, self.a)

    def handle_take_profit_2(self):
        self.cancel_stop_loss_2_order()
        self.update_pnl(self.take_profit_2, self.b)
        self.destroy()

    def handle_stop_loss_1(self):
        self.cancel_take_profit_1_order()
        self.update_pnl(self.stop_loss, self.a)

    def handle_stop_loss_2(self):
        self.cancel_take_profit_2_order()
        self.update_pnl(self.stop_loss, self.b)
        self.destroy()

    def fill_handle(self, event):
        client_id = event['c']
        if client_id in self.action_dict.keys():
            self.action_dict[client_id]()
        else:
            return

    def handle(self, event):
        try:
            if event['c'] not in self.action_dict.keys():
                return
            if event['X'] == CANCELED:
                self.destroy()
                log_fail(self.limit_order['clientOrderId'], 'Order be cancel')
            elif event['X'] == FILL:
                self.fill_handle(event)
        except (BinanceAPIException, BinanceRequestException):
            log_fail(self.limit_order['clientOrderId'], str(sys.exc_info()[1]))
            msg_box(sys.exc_info()[1])

    def update_pnl(self, price, percent):
        self.pnl = self.pnl + percent * (price - self.e) * self.margin / self.e

    # ----------------------------------------------------------------------------------------------------
    # Create Order
    # ----------------------------------------------------------------------------------------------------
    def make_stop_loss_1_order(self):
        parameter = get_stop_loss_form_limit(self.limit_order, self.stop_loss, self.a)
        order = open_order(self.client, parameter)
        limit_id = order['clientOrderId']
        self.replace_key(limit_id, 'stop1')

    def make_stop_loss_2_order(self):
        parameter = get_stop_loss_form_limit(self.limit_order, self.stop_loss, self.a)
        order = open_order(self.client, parameter)
        limit_id = order['clientOrderId']
        self.replace_key(limit_id, 'stop2')

    def make_take_profit_1_order(self):
        parameter = get_take_profit_form_limit(self.limit_order, self.take_profit_1, self.a)
        order = open_order(self.client, parameter)
        limit_id = order['clientOrderId']
        self.replace_key(limit_id, 'take1')

    def make_take_profit_2_order(self):
        parameter = get_take_profit_form_limit(self.limit_order, self.take_profit_2, self.b)
        order = open_order(self.client, parameter)
        limit_id = order['clientOrderId']
        self.replace_key(limit_id, 'take2')

    # ----------------------------------------------------------------------------------------------------
    # Cancel Order
    # ----------------------------------------------------------------------------------------------------
    def cancel_stop_loss_1_order(self):
        order_id = list(self.action_dict.keys())[1]
        if order_id == 'stop2':
            return
        self.client.futures_cancel_order(
            symbol=self.s,
            orderId=order_id
        )

    def cancel_stop_loss_2_order(self):
        order_id = list(self.action_dict.keys())[2]
        if order_id == 'stop2':
            return
        self.client.futures_cancel_order(
            symbol=self.s,
            orderId=order_id
        )

    def cancel_take_profit_1_order(self):
        order_id = list(self.action_dict.keys())[3]
        if order_id == 'take1':
            return
        self.client.futures_cancel_order(
            symbol=self.s,
            orderId=order_id
        )

    def cancel_take_profit_2_order(self):
        order_id = list(self.action_dict.keys())[4]
        if order_id == 'take2':
            return
        self.client.futures_cancel_order(
            symbol=self.s,
            orderId=order_id
        )

    def replace_key(self, new_key, old_key):
        if old_key in self.action_dict:
            # Tạo một dictionary mới để lưu trữ các phần tử
            new_dict = OrderedDict()
            # Duyệt qua tất cả các phần tử trong dictionary ban đầu
            for key, value in self.action_dict.items():
                if key == old_key:
                    # Thêm phần tử mới vào cùng vị trí với phần tử cũ
                    new_dict[new_key] = value
                else:
                    new_dict[key] = value
            self.action_dict = new_dict
        else:
            return
