from PyQt5.QtWidgets import QMessageBox
from binance.helpers import round_step_size


def check_val_data(data, msg_box):
    if type(data) == list:
        for value in data:
            if value == 0.0:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle("Lỗi")
                msg.setText(msg_box)
                msg.exec_()
                return False
        return True
    if type(data) == int or type(data) == float:
        if data == 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Lỗi")
            msg.setText(msg_box)
            msg.exec_()
            return False
        return True
    return True


def pre_proces(budgets, orders, stop_loss, take_profit, take_profit2, margin):
    if not check_val_data(budgets, "Trong budget có giá trị bằng 0"):
        return False
    if not check_val_data(orders, "Trong order có giá trị bằng 0"):
        return False
    if not check_val_data(stop_loss, "Chưa cài stop loss"):
        return False
    if not check_val_data(take_profit, "Chưa cài take_profit"):
        return False
    if not check_val_data(take_profit2, "Chưa cài take_profit2"):
        return False
    if not check_val_data(margin, "Chưa cài margin"):
        return False
    # all success
    return True


def process(data):
    requests = []
    data, open_type = data
    budgets, orders = data['m_list'], data['n_list']

    if not pre_proces(budgets, orders, data['sl'], data['tp1'], data['tp2'], data['margin']):
        return False, []

    for i in range(len(orders)):
        symbol = data['symbol']
        price = round_step_size(orders[i], 0.10)
        quantity = round(budgets[i] / price, 3)

        stop_loss = round_step_size(data['sl'], 0.10)
        take_profit_1 = round_step_size(data['tp1'], 0.10)
        take_profit_2 = round_step_size(data['tp2'], 0.10)

        a_quantity = round(quantity*data['a'], 3)
        b_quantity = quantity - a_quantity

        if a_quantity < 0.001 or b_quantity < 0.001:
            a_quantity = quantity
            b_quantity = 0

        margin = data['margin']
        requests.append(
            (symbol,
             quantity,
             price,
             stop_loss,
             take_profit_1,
             a_quantity,
             take_profit_2,
             b_quantity,
             margin,
             open_type))

    return True, requests
