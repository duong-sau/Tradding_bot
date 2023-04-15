import exrex


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
