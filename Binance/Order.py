import sys
import time

from PyQt5.QtWidgets import QMessageBox


def inflect_side(side):
    if side == "BUY":
        return "SELL"
    else:
        return "BUY"


class COrder:
    def __init__(self, client):
        self.client = client

    def open_order(self, symbol, quantity, price, stop_loss, take_profit, margin, side):
        try:
            self.client.futures_change_leverage(symbol=symbol, leverage=margin, timestamp=time.time())
            limit_order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                price=price,
                leverage=margin,
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
                reduceOnly=True,
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
                reduceOnly=True,
                type='TAKE_PROFIT_MARKET',
                newOrderRespType="ACK",
                timestamp=time.time()
            )
            print(limit_order, stop_loss_order, take_profit_order)
        except Exception:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Lỗi")
            msg.setText(sys.exc_info()[1])
            msg.exec_()
