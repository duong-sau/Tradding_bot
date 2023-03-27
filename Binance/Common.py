import inspect

import exrex

from binance.helpers import round_step_size

from Logic.Log import log_order


def get_rounded_price(price: float) -> float:
    return round_step_size(price, 0.10)


def inflect_side(side):
    if side == "BUY":
        return "SELL"
    else:
        return "BUY"


def get_limit_from_parameter(symbol, quantity, price, margin, side):
    order_id = exrex.getone(r'vduongsauv[a-z0-9]{12}')
    price = get_rounded_price(price)
    order_param = {
        'symbol': symbol,
        'side': side,
        'price': float(round(price, 2)),
        'quantity': float(round(quantity / price, 3)),
        'leverage': margin,
        'type': 'LIMIT',
        'newClientOrderId': order_id,
        'reduceOnly': False,
        'timeInForce': 'GTC',
        'newOrderRespType': "ACK"
    }
    return order_param


def get_stop_loss_form_limit(limit_order, stop_loss, percent):
    limit_side = limit_order['side']
    order_id = exrex.getone(r'vduongsauv[a-z0-9]{12}')
    stop_loss = get_rounded_price(stop_loss)
    order_param = {
        'symbol': limit_order['symbol'],
        'side': inflect_side(limit_side),
        'quantity': float(limit_order['origQty']) * percent,
        'stopPrice': float(round(stop_loss, 2)),
        'newClientOrderId': order_id,
        'reduceOnly': True,
        'type': 'STOP_MARKET',
        'newOrderRespType': "ACK"
    }
    return order_param


def get_take_profit_form_limit(limit_order, take_profit, percent):
    limit_side = limit_order['side']
    order_id = exrex.getone(r'vduongsauv[a-z0-9]{12}')
    take_profit = get_rounded_price(take_profit)
    order_param = {
        'symbol': limit_order['symbol'],
        'side': inflect_side(limit_side),
        'quantity': float(limit_order['origQty']) * percent,
        'stopPrice': float(round(take_profit, 2)),
        'newClientOrderId': order_id,
        'reduceOnly': True,
        'type': 'TAKE_PROFIT_MARKET',
        'newOrderRespType': "ACK"
    }
    return order_param


def open_order(client, data):
    order = client.futures_create_order(**data)
    order_id = order['clientOrderId']
    action = inspect.getouterframes(inspect.currentframe())[1][3]
    symbol = "BTCUSDT"
    profit = 0
    quantity = data['quantity']
    margin = 1
    try:
        price = data['price']
    except:
        price = data['stopPrice']
    try:
        margin = data['leverage']
    except:
        margin = 0
    log_order(action=action, order_id=order_id, symbol=symbol, profit=profit, quantity=quantity, margin=margin,
              price=price)
    return order