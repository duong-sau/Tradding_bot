import logging


def init_log():
    # Tạo log file và log stream
    log_file = "log.txt"
    log_stream = logging.FileHandler(log_file)

    # Cấu hình log stream
    log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log_stream.setFormatter(log_format)

    # Lấy logger của thư viện muốn đọc log
    library_logger = logging.getLogger('Tên_Logger_Của_Thư_Viện')

    # Đặt log level cho logger
    library_logger.setLevel(logging.DEBUG)

    # Gán log stream cho logger
    library_logger.addHandler(log_stream)

    # Sử dụng thư viện và ghi log
    # ...
