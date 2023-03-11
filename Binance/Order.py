import sys
import time


def inflect_side(side):
    if side == "BUY":
        return "SELL"
    else:
        return "BUY"


class COrder:
    def __init__(self, client):
        self.client = client

    def open_position(self, symbol, side, quantity, margin):
        try:
            self.client.futures_change_leverage(symbol=symbol, leverage=margin, timestamp=time.time())
            position = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                quantity=quantity,
                type='MARKET',
                leverage=margin,
                newOrderRespType="FULL",
                timestamp=time.time()
            )
            print(position)
        except Exception:
            print(sys.exc_info()[1])

    def open_order(self, symbol, quantity, price, stop_loss, take_profit, side):
        try:
            limit_order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                price=price,
                quantity=quantity,
                type='LIMIT',
                timeInForce='GTC',
                newOrderRespType="ACK",
                timestamp=time.time()
            )
            stop_loss_order = self.client.futures_create_order(
                symbol=symbol,
                side=inflect_side(side),
                quantity=quantity,
                stopPrice=stop_loss,
                type='STOP_MARKET',
                newOrderRespType="ACK",
                timestamp=time.time()
            )
            take_profit_order = self.client.futures_create_order(
                symbol=symbol,
                side=inflect_side(side),
                quantity=quantity,
                stopPrice=take_profit,
                type='TAKE_PROFIT_MARKET',
                newOrderRespType="ACK",
                timestamp=time.time()
            )
            print(limit_order, stop_loss_order, take_profit_order)
        except Exception:
            print(sys.exc_info()[1])
