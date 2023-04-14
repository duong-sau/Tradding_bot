from Binance.Order.Order import Order


class LimitOrder(Order):

    def __init__(self, parameter) -> None:
        super().__init__(parameter)
