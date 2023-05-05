from PyQt5.QtWidgets import QMessageBox
from binance.helpers import round_step_size

from View.a_common.MsgBox import msg_box


def check_list_data(data, message):
    for value in data:
        if value == 0.0:
            msg_box(message, "Lỗi")
            return False
    return True


def check_val_data(data, message):
    if data == 0:
        msg_box(message, "Lỗi")
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


def confirm_order(data):
    confirm_str = ""
    data
    for quantity, price in zip(data['m_list'], data['n_list']):
        confirm_str = confirm_str + f'Giá: {price}    |||| số lượng {quantity}\n'

    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setWindowTitle("Xác nhận đặt lệnh")
    msg.setText(confirm_str)
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    if msg.exec() != QMessageBox.Ok:
        return False
    return True


def process(data):
    requests = []
    data, open_type = data
    if not confirm_order(data):
        return False, []
    budgets, orders = data['m_list'], data['n_list']

    if not pre_proces(budgets, orders, data['margin']):
        return False, []

    for i in range(len(orders)):
        symbol = data['symbol']
        margin = data['margin']

        price = round_step_size(orders[i], 0.1)
        quantity = round(budgets[i] / price, 3)
        if quantity < 0.001:
            msg_box("Trong budget có giá trị bằng 0", "Lỗi")
            return False, []
        sl = data['sl']
        a = data['a']
        a = round(quantity * a, 3)
        tp1 = data['tp1']
        b = data['b']
        b = round(quantity * b, 3)
        tp2 = data['tp2']
        if a >= 0.001:
            requests.append(
                (symbol,
                 a,
                 price,
                 tp1,
                 sl,
                 margin,
                 open_type))
        if b >= 0.001:
            requests.append(
                (symbol,
                 b,
                 price,
                 tp2,
                 sl,
                 margin,
                 open_type))
    requests = sorted(requests, key=lambda x: x[2])
    if open_type == "BUY":
        requests.reverse()

    return True, requests
