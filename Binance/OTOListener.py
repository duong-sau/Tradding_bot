import sys
from collections import OrderedDict
from binance.exceptions import BinanceRequestException, BinanceAPIException

from Binance.Common import get_stop_loss_form_limit, get_take_profit_form_limit, open_order
from Logic.Log import log_order, log_fail, log_fill, log_cancel
from View.a_common.MsgBox import msg_box

CANCELED = 'CANCELED'
FILL = 'FILLED'


class OTOListener:
    def __init__(self, client, destroy_call_back, cancel_call_back, parameter,
                 stop_loss, take_profit, a_quantity, take_profit_2, b_quantity) -> None:

        self.limit_order = None
        self.destroy_call_back = destroy_call_back
        self.cancel_all_call_back = cancel_call_back

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
        self.state = ""

        self.client = client
        self.parameter = parameter

        self.stop_loss = stop_loss

        self.take_profit_1 = take_profit
        self.a_quantity = a_quantity

        self.take_profit_2 = take_profit_2
        self.b_quantity = b_quantity

        return

    def destroy(self):
        log_fail(self.parameter['newClientOrderId'], "Destroy")
        self.destroy_call_back(self)
        pass

    def make_limit_order(self):
        try:
            self.state = "OPEN"
            limit_order = open_order(self.client, self.parameter, self.parameter['newClientOrderId'])
            self.limit_order = limit_order
            limit_id = limit_order['orderId']
            self.replace_key(limit_id, 'limit')

        except(BinanceRequestException, BinanceAPIException):
            error = str(sys.exc_info()[1])
            log_fail(self.parameter['newClientOrderId'], error)
            msg_box(error)
            self.destroy()

    def handle_limit(self, ap):
        self.state = "V1"
        self.e = float(ap)
        self.make_stop_loss_1_order()
        self.make_take_profit_1_order()

        if self.b_quantity != 0:
            self.make_stop_loss_2_order()
            self.make_take_profit_2_order()

    def handle_take_profit_1(self, ap):
        self.state = 'V2'
        self.cancel_stop_loss_1_order()
        self.update_pnl(self.take_profit_1, self.a_quantity)
        log_fill(limit_order_id=self.limit_order['clientOrderId'], order_id=list(self.action_dict.keys())[3],
                 profit=self.pnl, symbol=self.parameter['symbol'])
        if self.b_quantity == 0:
            self.destroy()

    def handle_take_profit_2(self, ap):
        self.cancel_stop_loss_2_order()
        self.update_pnl(self.take_profit_2, self.b_quantity)
        log_fill(limit_order_id=self.limit_order['clientOrderId'], order_id=list(self.action_dict.keys())[4],
                 profit=self.pnl, symbol=self.parameter['symbol'])
        self.cancel_all_call_back()
        self.destroy()

    def handle_stop_loss_1(self, ap):
        self.state = 'V2'
        self.cancel_take_profit_1_order()
        self.update_pnl(self.stop_loss, self.a_quantity)
        log_fill(limit_order_id=self.limit_order['clientOrderId'], order_id=list(self.action_dict.keys())[1],
                 profit=self.pnl, symbol=self.parameter['symbol'])
        if self.b_quantity == 0:
            self.destroy()

    def handle_stop_loss_2(self, ap):
        self.cancel_take_profit_2_order()
        self.update_pnl(self.stop_loss, self.b_quantity)
        log_fill(limit_order_id=self.limit_order['clientOrderId'], order_id=list(self.action_dict.keys())[2],
                 profit=self.pnl, symbol=self.parameter['symbol'])
        self.cancel_all_call_back()
        self.destroy()

    def fill_handle(self, event):
        client_id = event['i']
        if client_id in self.action_dict.keys():
            self.action_dict[client_id](ap=event['ap'])
        else:
            return

    def handle(self, event):
        try:
            if event['i'] not in self.action_dict.keys():
                return
            if event['X'] == CANCELED:
                self.destroy()
                log_fail(self.limit_order['clientOrderId'], 'Order be cancel')
            elif event['X'] == FILL:
                self.fill_handle(event)
        except (BinanceAPIException, BinanceRequestException):
            msg_box(sys.exc_info()[1])

    def update_pnl(self, price, percent):
        if self.parameter['side'] != 'BUY':
            percent = -percent
        self.pnl = self.pnl + percent * (price - self.e) * self.margin

    # ----------------------------------------------------------------------------------------------------
    # Create Order
    # ----------------------------------------------------------------------------------------------------
    def make_stop_loss_1_order(self):
        try:
            parameter = get_stop_loss_form_limit(self.limit_order, self.stop_loss, self.a_quantity)
            order = open_order(self.client, parameter, self.limit_order['clientOrderId'])
            limit_id = order['orderId']
            self.replace_key(limit_id, 'stop1')
        except:
            log_fail(self.limit_order['clientOrderId'], str(sys.exc_info()[1]))
            raise

    def make_stop_loss_2_order(self):
        try:
            if self.b_quantity < 0.01:
                return
            parameter = get_stop_loss_form_limit(self.limit_order, self.stop_loss, self.b_quantity)
            order = open_order(self.client, parameter, self.limit_order['clientOrderId'])
            limit_id = order['orderId']
            self.replace_key(limit_id, 'stop2')
        except:
            log_fail(self.limit_order['clientOrderId'], str(sys.exc_info()[1]))
            raise

    def make_take_profit_1_order(self):
        try:
            parameter = get_take_profit_form_limit(self.limit_order, self.take_profit_1, self.a_quantity)
            order = open_order(self.client, parameter, self.limit_order['clientOrderId'])
            limit_id = order['orderId']
            self.replace_key(limit_id, 'take1')
        except:
            log_fail(self.limit_order['clientOrderId'], str(sys.exc_info()[1]))
            raise

    def make_take_profit_2_order(self):
        try:
            if self.b_quantity < 0.001:
                return
            parameter = get_take_profit_form_limit(self.limit_order, self.take_profit_2, self.b_quantity)
            order = open_order(self.client, parameter, self.limit_order['clientOrderId'])
            limit_id = order['orderId']
            self.replace_key(limit_id, 'take2')
        except:
            log_fail(self.limit_order['clientOrderId'], str(sys.exc_info()[1]))
            raise

    # ----------------------------------------------------------------------------------------------------
    # Cancel Order
    # ----------------------------------------------------------------------------------------------------
    def cancel_limit_order(self):
        order_id = list(self.action_dict.keys())[0]
        if order_id == 'limit':
            return
        self.client.futures_cancel_order(
            symbol=self.s,
            origClientOrderId=order_id
        )
        log_cancel(limit_order_id=self.limit_order['clientOrderId'], order_id=order_id,
                   symbol=self.limit_order['symbol'])

    def cancel_stop_loss_1_order(self):
        order_id = list(self.action_dict.keys())[1]
        if order_id == 'stop1':
            return
        self.client.futures_cancel_order(
            symbol=self.s,
            OrderId=order_id
        )
        log_cancel(limit_order_id=self.limit_order['clientOrderId'], order_id=order_id,
                   symbol=self.limit_order['symbol'])

    def cancel_stop_loss_2_order(self):
        order_id = list(self.action_dict.keys())[2]
        if order_id == 'stop2':
            return
        self.client.futures_cancel_order(
            symbol=self.s,
            OrderId=order_id
        )
        log_cancel(limit_order_id=self.limit_order['clientOrderId'], order_id=order_id,
                   symbol=self.limit_order['symbol'])

    def cancel_take_profit_1_order(self):
        order_id = list(self.action_dict.keys())[3]
        if order_id == 'take1':
            return
        self.client.futures_cancel_order(
            symbol=self.s,
            OrderId=order_id
        )
        log_cancel(limit_order_id=self.limit_order['clientOrderId'], order_id=order_id,
                   symbol=self.limit_order['symbol'])

    def cancel_take_profit_2_order(self):

        order_id = list(self.action_dict.keys())[4]
        if order_id == 'take2':
            return
        self.client.futures_cancel_order(
            symbol=self.s,
            OrderId=order_id
        )
        log_cancel(limit_order_id=self.limit_order['clientOrderId'], order_id=order_id,
                   symbol=self.limit_order['symbol'])

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

    def get_pnl(self, price):
        if self.parameter['side'] == 'BUY':
            b_quantity = self.b_quantity
            m = self.m
        else:
            b_quantity = -self.b_quantity
            m = - self.m

        if self.state == "OPEN":
            pnl = 0
        elif self.state == "V1":
            pnl = m * (price - self.e) * self.margin
        elif self.state == "V2":
            pnl = self.pnl + b_quantity * (price - self.e) * self.margin
        else:
            pnl = 0
        return pnl

    def cancel_all(self):
        if self.state == "OPEN":
            self.cancel_limit_order()
