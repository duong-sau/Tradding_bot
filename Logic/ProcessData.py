from PyQt5.QtWidgets import QMessageBox

from common import math_dict


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


def complete_data(data):
    m = data['M']
    n = data['n']
    min_val = data['min']
    max_val = data['max']
    m_ = data['m_']
    n_ = data['n_']
    m_list = math_dict[m_](min_val=0, max_val=m, counter=n)
    n_list = math_dict[n_](min_val=min_val, max_val=max_val, counter=n)
    data['M'] = m_list
    data['n'] = n_list
    return data


def process(data):
    requests = []
    data, open_type = data
    data = complete_data(data)
    budgets, orders = data['M'], data['n']

    if not pre_proces(budgets, orders, data['sl'], data['tp1'], data['tp2'], data['margin']):
        return False, []

    for i in range(len(orders)):
        requests.append((data['symbol'], budgets[i], orders[i], data['sl'], data['tp1'], data['tp2'],data['margin'], open_type))
    return True, requests
