import json
import subprocess

from PyQt5.QtWidgets import QMessageBox
from binance.helpers import round_step_size

from Source.View.Binance import get_tick_price


def confirm_order(datas):
    confirm_str = ""
    for data in datas:
        symbol, price, margin, side, a, b, sl, tp1, tp2 = data['symbol'], data['price'], data['margin'], data['side'], \
        data['a'], data['b'], data['sl'], data['tp1'], data['tp2']
        confirm_str = confirm_str + f'Giá: {round(price, 2)}   |||| số lượng {round(a + b, 3)}\n'

    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setWindowTitle("Xác nhận đặt lệnh")
    msg.setText(confirm_str)
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    if msg.exec() != QMessageBox.Ok:
        return False
    return True


def open_order(side, data):
    result, data = process(side, data)
    if not result:
        return
    if not confirm_order(data):
        return
    data_dict = {"DCA": data}
    file = open('biance_test.json', mode='w')
    json.dump(data_dict, file)
    file.close()
    subprocess.Popen(['python', r'C:\Users\phamv\Downloads\Bot\Bot\BinaceMain.py'])


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


def process(side, data):
    requests = []
    budgets, orders = data['m_list'], data['n_list']

    PricePrecision, QuantityPrecision = get_tick_price(data['symbol'])

    if not pre_proces(budgets, orders, data['sl'], data['tp1'], data['tp2'], data['margin']):
        return False, []

    for i in range(len(orders)):
        symbol = data['symbol']
        margin = data['margin']

        price = round_step_size(orders[i], PricePrecision)
        quantity = round_step_size(budgets[i] / price, QuantityPrecision)

        stop_loss = round_step_size(data['sl'], PricePrecision)
        tp1 = round_step_size(data['tp1'], PricePrecision)
        tp2 = round_step_size(data['tp2'], PricePrecision)

        a_quantity = round_step_size(quantity * data['a'], QuantityPrecision)
        b_quantity = round_step_size(quantity - a_quantity, QuantityPrecision)

        if a_quantity < QuantityPrecision or b_quantity < QuantityPrecision:
            a_quantity = quantity
            b_quantity = 0

        requests.append(
            dict(symbol=symbol,
                 quantity=quantity,
                 side=side,
                 price=price,
                 sl=stop_loss,
                 tp1=tp1,
                 a=a_quantity,
                 tp2=tp2,
                 b=b_quantity,
                 margin=margin, )
        )
        # symbol, price, margin, side, a, b, sl, tp1, tp2
        # requests.append(
        #     (symbol, price, margin, open_type, a_quantity, b_quantity, stop_loss, take_profit_1, take_profit_2)
        # )
    return True, requests
