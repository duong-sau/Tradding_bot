from binance.exceptions import BinanceAPIException

from Binance.Common.Common import convert_data_to_parameters
from Binance.Order.LimitOrder import LimitOrder
from Binance.Order.StopMarketOrder import StopMarketOrder
from Binance.Strage.OTOCO import OTOCO


class PositionBatch:
    def __init__(self, datas):
        self.position_list = []
        for data in datas:
            symbol, quantity, price, take_profit, stop_loss, margin, side = data
            limit_parameter, take_parameter, stop_parameter = convert_data_to_parameters(symbol, quantity, price,
                                                                                         take_profit, stop_loss, margin,
                                                                                         side)
            limit_order = LimitOrder(limit_parameter)
            take_order = StopMarketOrder(take_parameter)
            stop_order = StopMarketOrder(stop_parameter)

            position = OTOCO(limit_order, take_order, stop_order, self.remove_position, self.cancel_all)
            self.position_list.append(position)

    def cancel_all(self):
        for position in self.position_list:
            try:
                position.cancel()
            except BinanceAPIException as e:
                if e.code == -2011:
                    print('2011')

    def remove_position(self, position):
        self.position_list.remove(position)

    def place(self):
        for position in self.position_list:
            position.place()

    def handel(self, event):
        for position in self.position_list:
            position.handel(event)
