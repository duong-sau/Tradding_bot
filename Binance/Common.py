import sys

import exrex
from PyQt5.QtWidgets import QMessageBox
from binance.exceptions import BinanceRequestException, BinanceAPIException

from Telegram.TelegramThread import error_notification


def inflect_side(side):
    if side == "BUY":
        return "SELL"
    else:
        return "BUY"


def get_limit_from_parameter(symbol, quantity, price, margin, side):
    order_id = exrex.getone(r'vduongsauv[a-z0-9]{12}')
    if side == "BUY":
        position_side = "LONG"
    else:
        position_side = "SHORT"
    order_param = {
        'symbol': symbol,
        'side': side,
        'price': price,
        'quantity': quantity,
        'leverage': margin,
        'type': 'LIMIT',
        'newClientOrderId': order_id,
        'positionSide': position_side,
        'timeInForce': 'GTC',
        'newOrderRespType': "ACK"
    }
    return order_param


def get_stop_loss_from_parameter(symbol, quantity, price, side):
    order_id = exrex.getone(r'vduongsauv[a-z0-9]{12}')
    if side == "BUY":
        position_side = "LONG"
    else:
        position_side = "SHORT"
    order_param = {
        'symbol': symbol,
        'side': inflect_side(side),
        'quantity': quantity,
        'stopPrice': price,
        'newClientOrderId': order_id,
        'positionSide': position_side,
        'type': 'STOP_MARKET',
        'newOrderRespType': "ACK"
    }
    return order_param


def get_take_profit_from_parameter(symbol, quantity, price, side):
    order_id = exrex.getone(r'vduongsauv[a-z0-9]{12}')
    if side == "BUY":
        position_side = "LONG"
    else:
        position_side = "SHORT"
    order_param = {
        'symbol': symbol,
        'side': inflect_side(side),
        'quantity': quantity,
        'stopPrice': price,
        'newClientOrderId': order_id,
        'positionSide': position_side,
        'type': 'TAKE_PROFIT_MARKET',
        'newOrderRespType': "ACK"
    }
    return order_param


def open_limit(client, symbol, quantity, price, margin, side):
    data = get_limit_from_parameter(symbol, quantity, price, margin, side)
    order = client.futures_create_order(**data)
    return order['orderId']


def open_take_profit(client, symbol, quantity, price, side):
    try:
        data = get_take_profit_from_parameter(symbol, quantity, price, side)
        order = client.futures_create_order(**data)
        return order['orderId']
    except(BinanceRequestException, BinanceAPIException):
        error = str(sys.exc_info()[1])
        error_notification(error)


def open_stop_loss(client, symbol, quantity, price, side):
    try:
        data = get_stop_loss_from_parameter(symbol, quantity, price, side)
        order = client.futures_create_order(**data)
        return order['orderId']
    except(BinanceRequestException, BinanceAPIException):
        error = str(sys.exc_info()[1])
        error_notification(error)


def cancel_order(client, symbol, order_id):
    try:
        client.futures_cancel_order(
            symbol=symbol,
            orderId=order_id
        )
    except:
        pass


def confirm_order(datas):
    confirm_str = ""
    for data in datas:
        symbol, price, stop_loss, take_profit_1, a, take_profit_2, b, margin, side = data
        confirm_str = confirm_str + f'Giá: {price}    |||| số lượng {a + b}\n'

    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setWindowTitle("Xác nhận đặt lệnh")
    msg.setText(confirm_str)
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    if msg.exec() != QMessageBox.Ok:
        return False
    return True
