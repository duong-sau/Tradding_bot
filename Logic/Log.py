import pygsheets

# Đường dẫn đến file JSON chứa thông tin Service Account Key
path_to_json_file = r'C:\Users\phamv\Downloads\Bot\Bot\Logic\traddingbot-18675fbbd1d6.json'

# Khởi tạo một kết nối đến Google Sheets bằng Pygsheets
gc = pygsheets.authorize(service_file=path_to_json_file)

# Lấy một worksheet bằng tên của worksheet đó
work_book = gc.open_by_key('1qrSDPFVZYW2k1oJGgrTqbPlfzp17wbM2q6Nua8aFUP4')
log = work_book.worksheet(property='title', value='order_log')


def log_order(order_id, action, symbol, price, quantity, margin, profit):
    new_row_values = [order_id, action, symbol, price, quantity, margin, profit]
    log.append_table(values=[new_row_values])


def log_fail(limit_id, content):
    row = [limit_id, content]
    log.append_table(values=[row])

if __name__ == '__main__':
    log_order('1', 2, 3, 4, 5, 6, 7)
    log_fail('1234', 'fail')