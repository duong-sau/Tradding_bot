import exrex


def inflect_side(side):
    if side == "BUY":
        return "SELL"
    else:
        return "BUY"


def get_limit_from_parameter(symbol, quantity, price, margin, side):
    order_id = exrex.getone(r'vduongsauv[a-z0-9]{12}')
    order_param = {
        'symbol': symbol,
        'side': side,
        'price': price,
        'quantity': quantity,
        'leverage': margin,
        'type': 'LIMIT',
        'newClientOrderId': order_id,
        'reduceOnly': False,
        'timeInForce': 'GTC',
        'newOrderRespType': "ACK"
    }
    return order_param


def get_stop_loss_form_limit(limit_order, stop_loss):
    limit_side = limit_order['side']
    order_id = exrex.getone(r'vduongsauv[a-z0-9]{12}')
    order_param = {
        'symbol': limit_order['symbol'],
        'side': inflect_side(limit_side),
        'quantity': limit_order['origQty'],
        'stopPrice': stop_loss,
        'newClientOrderId': order_id,
        'reduceOnly': True,
        'type': 'STOP_MARKET',
        'newOrderRespType': "ACK"
    }
    return order_param


def get_take_profit_form_limit(limit_order, take_profit):
    limit_side = limit_order['side']
    order_id = exrex.getone(r'vduongsauv[a-z0-9]{12}')
    order_param = {
        'symbol': limit_order['symbol'],
        'side': inflect_side(limit_side),
        'quantity': limit_order['origQty'],
        'stopPrice': take_profit,
        'newClientOrderId': order_id,
        'reduceOnly': True,
        'type': 'TAKE_PROFIT_MARKET',
        'newOrderRespType': "ACK"
    }
    return order_param
