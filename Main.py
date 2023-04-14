import datetime
import sys
import traceback
from socket import gethostname
from PyQt5.QtWidgets import QApplication
from qt_material import apply_stylesheet

from Binance.BianceThread import CBinanceThread
from Logic.CLogicThread import CLogicThread
from View.MainView import MainWindow
from connection import register_connections


def handle_exception(exc_type, exc_value, exc_traceback):
    # In ra thông báo lỗi và traceback
    print("Unhandled exception:", exc_value)


# Đăng ký hàm xử lý ngoại lệ cho toàn bộ ứng dụng Python
sys.excepthook = handle_exception

if __name__ == '__main__':

    app = QApplication(sys.argv)
    extra = {
        # Font
        'font_family': 'Consolas',
        'font_size': 20
    }

    apply_stylesheet(app, theme='dark_yellow.xml', invert_secondary=True, extra=extra)

    # logic thread
    logic_thread = CLogicThread()

    # binance thread
    binance_thread = CBinanceThread()


    # Window thread
    mainWindow = MainWindow()

    try:
        # connection
        register_connections(binance_thread, logic_thread, mainWindow)

        logic_thread.start()
        binance_thread.start()

        # View
        mainWindow.show()
        binance_thread.set_symbols()

    except Exception:
        traceback.print_exc()

        # stop
        binance_thread.stop()
        logic_thread.stop()

        # exit
        app.exit(0)
    try:
        error = app.exec()
        binance_thread.stop()
        logic_thread.stop()
        sys.exit(0)
    except:
        print('exit')
