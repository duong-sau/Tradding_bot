from binance.helpers import round_step_size

from View.a_common.MsgBox import msg_box


def check_list_data(data, message):
    for value in data:
        if value == 0.0:
            msg_box("Lỗi", message)
            return False
    return True


def check_val_data(data, message):
    if data == 0:
        msg_box("Lỗi", message)
        return False
    return True


def pre_proces(budgets, orders, margin):
    if not check_list_data(budgets, "Trong budget có giá trị bằng 0"):
        return False
    if not check_list_data(orders, "Trong order có giá trị bằng 0"):
        return False
    if not check_val_data(margin, "Chưa cài margin"):
        return False
    # all success
    return True


def process(data):
    requests = []
    data, open_type = data
    budgets, orders = data['m_list'], data['n_list']

    if not pre_proces(budgets, orders, data['margin']):
        return False, []

    for i in range(len(orders)):
        symbol = data['symbol']
        margin = data['margin']

        price = round_step_size(orders[i], 0.1)
        quantity = round(budgets[i] / price, 3)
        if quantity < 0.001:
            msg_box("Lỗi", "Trong budget có giá trị bằng 0")
            return False, []

        requests.append(
            (symbol,
             quantity,
             price,
             margin,
             open_type))

    return True, requests
