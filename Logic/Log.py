import asyncio
import inspect
import threading

import pygsheets

# Đường dẫn đến file JSON chứa thông tin Service Account Key
path_to_json_file = r'.\traddingbot-18675fbbd1d6.json'

# Khởi tạo một kết nối đến Google Sheets bằng Pygsheets
gc = pygsheets.authorize(service_file=path_to_json_file)

# Lấy một worksheet bằng tên của worksheet đó
work_book = gc.open_by_key('1qrSDPFVZYW2k1oJGgrTqbPlfzp17wbM2q6Nua8aFUP4')
log = work_book.worksheet(property='title', value='order_log')


def log_order(limit_order_id, order_id, action, symbol, price, quantity, margin, profit):
    new_row_values = [limit_order_id, order_id, action, symbol, price, quantity, margin, profit]
    put_log(new_row_values)


def log_fill(limit_order_id, order_id, symbol, profit):
    action = inspect.getouterframes(inspect.currentframe())[1][3]
    new_row_values = [limit_order_id, order_id, "FILL", symbol, action, "", "", profit]
    put_log(new_row_values)


def log_cancel(limit_order_id, order_id, symbol, ):
    action = inspect.getouterframes(inspect.currentframe())[1][3]
    new_row_values = [limit_order_id, order_id, "CANCEL", symbol, action, "", "", ""]
    put_log(new_row_values)


def log_fail(limit_id, content):
    action = inspect.getouterframes(inspect.currentframe())[1][3]
    row = [limit_id, action, content]
    put_log(row)


def put_log(row):
    file = open(rf'.\log\{row[0]}.txt', mode='a')
    for dat in row:
        file.write(str(dat))
        file.write(', ')
    file.write('\n')
    file.close()
    # t = threading.Thread(target=log_wrap, args=(row,))
    # t.start()


def log_wrap(row):
    # log.append_table(values=[row])
    a = 0
