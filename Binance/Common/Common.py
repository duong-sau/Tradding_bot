import exrex
from binance.helpers import round_step_size


def get_rounded_price(price: float) -> float:
    return round_step_size(price, 0.10)


def inflect_side(side):
    if side == "BUY":
        return "SELL"
    else:
        return "BUY"


def convert_data_to_parameters(symbol, quantity, price, take_profit, stop_loss, margin, side, ):
    # LIMIT
    limit_id = exrex.getone(r'vduongsauv[a-z0-9]{12}')
    limit_param = {
        'symbol': symbol,
        'side': side,
        'price': price,
        'quantity': quantity,
        'leverage': margin,
        'type': 'LIMIT',
        'newClientOrderId': limit_id,
        'reduceOnly': False,
        'timeInForce': 'GTC',
        'newOrderRespType': "ACK"
    }
    # STOP LOSS
    stop_id = exrex.getone(r'vduongsauv[a-z0-9]{12}')
    stop_param = {
        'symbol': symbol,
        'side': inflect_side(side),
        'quantity': quantity,
        'stopPrice': stop_loss,
        'newClientOrderId': stop_id,
        'reduceOnly': True,
        'type': 'STOP_MARKET',
        'newOrderRespType': "ACK"
    }
    # TAKE PROFIT
    take_id = exrex.getone(r'vduongsauv[a-z0-9]{12}')
    take_param = {
        'symbol': symbol,
        'side': inflect_side(side),
        'quantity': quantity,
        'stopPrice': take_profit,
        'newClientOrderId': take_id,
        'reduceOnly': True,
        'type': 'TAKE_PROFIT_MARKET',
        'newOrderRespType': "ACK"
    }

    return limit_param, take_param, stop_param
