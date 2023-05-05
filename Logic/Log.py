from Logic import order_log_file, websocket_log_file


def put_log(row):
    for data in row:
        order_log_file.write(str(data))
    order_log_file.write('\n')


def put_log_socket(row):
    for data in row:
        websocket_log_file.write(str(data))
    websocket_log_file.write('\n')


def order_log(param):
    put_log([param])


def socket_log(param):
    put_log_socket([param])
