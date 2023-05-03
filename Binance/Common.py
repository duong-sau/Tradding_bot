import exrex


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


def get_stop_loss_form_limit(limit_order, stop_loss):
    limit_side = limit_order['side']
    if limit_side == "BUY":
        position_side = "LONG"
    else:
        position_side = "SHORT"
    order_id = exrex.getone(r'vduongsauv[a-z0-9]{12}')
    order_param = {
        'symbol': limit_order['symbol'],
        'side': inflect_side(limit_side),
        'quantity': limit_order['quantity'],
        'stopPrice': stop_loss,
        'newClientOrderId': order_id,
        'reduceOnly': True,
        'type': 'STOP_MARKET',
        'positionSide': position_side,
        'newOrderRespType': "ACK"
    }
    return order_param


CANCELED = "CANCELED"
FILLED = "FILLED"
