import inspect

import exrex
from PyQt5.QtWidgets import QMessageBox

from Logic.Log import log_order


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


def get_stop_loss_form_limit(limit_order, stop_loss, quantity):
    limit_side = limit_order['side']
    order_id = exrex.getone(r'vduongsauv[a-z0-9]{12}')
    order_param = {
        'symbol': limit_order['symbol'],
        'side': inflect_side(limit_side),
        'quantity': quantity,
        'stopPrice': stop_loss,
        'newClientOrderId': order_id,
        'reduceOnly': True,
        'type': 'STOP_MARKET',
        'newOrderRespType': "ACK"
    }
    return order_param


def get_take_profit_form_limit(limit_order, take_profit, quantity):
    limit_side = limit_order['side']
    order_id = exrex.getone(r'vduongsauv[a-z0-9]{12}')
    order_param = {
        'symbol': limit_order['symbol'],
        'side': inflect_side(limit_side),
        'quantity': quantity,
        'stopPrice': take_profit,
        'newClientOrderId': order_id,
        'reduceOnly': True,
        'type': 'TAKE_PROFIT_MARKET',
        'newOrderRespType': "ACK"
    }
    return order_param


def open_order(client, data, limit_order_id):
    order_id = data['newClientOrderId']
    action = inspect.getouterframes(inspect.currentframe())[1][3]
    symbol = data['symbol']
    profit = 0
    quantity = data['quantity']
    try:
        price = data['price']
    except:
        price = data['stopPrice']
    try:
        margin = data['leverage']
    except:
        margin = 0
    log_order(action=action, order_id=order_id, symbol=symbol, profit=profit, quantity=quantity, margin=margin,
              price=price, limit_order_id=limit_order_id)
    order = client.futures_create_order(**data)
    log_order(action='Make order success', order_id=order['clientOrderId'], symbol=symbol, profit=profit,
              quantity=quantity, margin=margin, price=price, limit_order_id=limit_order_id)
    return order


def confirm_order(datas):
    confirm_str = ""
    for data in datas:
        symbol, quantity, price, stop_loss, take_profit_1, a, take_profit_2, b, margin, side = data
        confirm_str = confirm_str + f'Giá: {price}    |||| số lượng {quantity}\n'

    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setWindowTitle("Xác nhận đặt lệnh")
    msg.setText(confirm_str)
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    if msg.exec() != QMessageBox.Ok:
        return False
    return True
