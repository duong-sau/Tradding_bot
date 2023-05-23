from binance.enums import ORDER_STATUS_CANCELED, ORDER_STATUS_FILLED, ORDER_STATUS_EXPIRED

from Source.Binance.Control.OTOListener import OTOListener
from Source.Telegram.TelegramThread import take_1_notification, take_2_notification, stop_notification, \
    start_notification, \
    end_notification, limit_notification


class Controller:
    controller_id = 0

    def __init__(self) -> None:
        super().__init__()
        self.position_list = []
        Controller.controller_id += 1
        self.id = Controller.controller_id

    def add_position(self, client, datas):
        for data in datas['DCA']:
            symbol, price, margin, side, a, b, sl, tp1, tp2 = data['symbol'], data['price'], data['margin'], data['side'], \
                data['a'], data['b'], data['sl'], data['tp1'], data['tp2']
            position = OTOListener(symbol, price, margin, side, a, b, sl, tp1, tp2)
            position.set_client(client)
            self.position_list.append(position)
            position.make_limit_order()
        start_notification(self.id)

    def handel(self, client, order_id, event):
        for position in self.position_list:
            if order_id in position.get_order_ids():
                position.set_client(client)
                self.control(order_id, event, position)

    def remove_position(self, position):
        self.position_list.remove(position)

    def control(self, order_id, event, position):
        '''
        TELEGRAM
        '''
        if event == ORDER_STATUS_FILLED:
            if order_id == position.tp1_order:
                take_1_notification(self.id, self.position_list.index(position) + 1)
            elif order_id == position.tp2_order:
                take_2_notification(self.id, self.position_list.index(position) + 1)
            elif order_id == position.sl1_order:
                stop_notification(self.id, self.position_list.index(position) + 1)
            elif order_id == position.limit_order:
                limit_notification(self.id, self.position_list.index(position) + 1)
        """
        Control
        """
        if event == ORDER_STATUS_CANCELED:
            if order_id in [position.limit_order, position.tp2_order, position.sl2_order]:
                self.remove_position(position)
            elif order_id in [position.tp1_order, position.sl1_order] and position.b == 0:
                self.remove_position(position)
        elif event == ORDER_STATUS_FILLED or event == ORDER_STATUS_EXPIRED:
            if order_id == position.limit_order:
                position.handel_limit()
            elif order_id == position.tp1_order:
                position.handle_take_profit_1()
            elif order_id == position.tp2_order:
                position.handle_take_profit_2()
            elif order_id == position.sl1_order:
                position.handle_stop_loss_1()
            elif order_id == position.sl2_order:
                position.handle_stop_loss_2()

        if len(self.position_list) == 0:
            end_notification(self.id)
