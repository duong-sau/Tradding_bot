import sys

import exrex
from PyQt5.QtWidgets import QMessageBox
from binance.exceptions import BinanceRequestException, BinanceAPIException

from Binance import symbol_size
from Telegram.TelegramThread import error_notification


def get_limit_from_parameter(symbol, quantity, price, margin, ps_side):
    if ps_side == 'LONG':
        side = 'BUY'
    else:
        side = 'SELL'
    order_id = exrex.getone(r'vduongsauv[a-z0-9]{12}')
    order_param = {
        'symbol': symbol,
        'side': side,
        'price': price,
        'quantity': quantity,
        'leverage': margin,
        'type': 'LIMIT',
        'newClientOrderId': order_id,
        'positionSide': ps_side,
        'timeInForce': 'GTC',
        'newOrderRespType': "ACK"
    }
    return order_param


def get_stop_loss_from_parameter(symbol, quantity, price, ps_side):
    if ps_side == 'LONG':
        side = 'SELL'
    else:
        side = 'BUY'
    order_id = exrex.getone(r'vduongsauv[a-z0-9]{12}')
    order_param = {
        'symbol': symbol,
        'side': side,
        'quantity': quantity,
        'stopPrice': price,
        'newClientOrderId': order_id,
        'positionSide': ps_side,
        'type': 'STOP_MARKET',
        'newOrderRespType': "ACK"
    }
    return order_param


def get_take_profit_from_parameter(symbol, quantity, price, ps_side):
    if ps_side == 'LONG':
        side = 'SELL'
    else:
        side = 'BUY'
    order_id = exrex.getone(r'vduongsauv[a-z0-9]{12}')
    order_param = {
        'symbol': symbol,
        'side': side,
        'quantity': quantity,
        'price': price,
        'newClientOrderId': order_id,
        'positionSide': ps_side,
        'timeInForce': 'GTC',
        'type': 'LIMIT',
        'newOrderRespType': "ACK"
    }
    return order_param


def get_market_from_parameter(symbol, quantity, ps_side):
    if ps_side == 'LONG':
        side = 'SELL'
    else:
        side = 'BUY'
    order_id = exrex.getone(r'vduongsauv[a-z0-9]{12}')
    order_param = {
        'symbol': symbol,
        'side': side,
        'quantity': quantity,
        'newClientOrderId': order_id,
        'positionSide': ps_side,
        'type': 'MARKET',
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
    except BinanceAPIException as e:
        error_code = e.code
        if error_code == -2021:
            force_stop_loss(client, symbol, quantity, side)
            return False
        else:
            error = str(sys.exc_info()[1])
            error_notification(error)
            return False


def force_stop_loss(client, symbol, quantity, side):
    try:
        data = get_market_from_parameter(symbol, quantity, side)
        client.futures_create_order(**data)
    except:
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
        symbol, price, margin, side, a, b, sl, tp1, tp2 = data
        confirm_str = confirm_str + f'Giá: {round(price, 2)}   |||| số lượng {round(a + b, 3)}\n'

    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setWindowTitle("Xác nhận đặt lệnh")
    msg.setText(confirm_str)
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    if msg.exec() != QMessageBox.Ok:
        return False
    return True


def get_tick_price(symbol):
    symbol_data = symbol_size
    config = symbol_data[symbol]
    return config[0], config[1]
