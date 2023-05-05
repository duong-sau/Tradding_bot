import datetime
import sys
import time
import traceback
from socket import gethostname

from PyQt5.QtWidgets import QApplication
from qt_material import apply_stylesheet

from Binance.BianceThread import CBinanceThread
from Binance.WebSocketThread import CSocketThread
from Logic.CLogicThread import CLogicThread
from Logic.Log import log_fail
from View.MainView import MainWindow
from connection import register_connections
import sys

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

    # socket thread
    socket_thread = CSocketThread()

    # Window thread
    mainWindow = MainWindow()

    try:
        # connection
        register_connections(binance_thread, logic_thread, socket_thread, mainWindow)

        logic_thread.start()
        binance_thread.start()
        socket_thread.start()

        # View
        mainWindow.show()
        binance_thread.set_symbols()

    except Exception:
        # error
        log_fail("System exit", str(sys.exc_info()[1]))
        traceback.print_exc()

        # stop
        binance_thread.stop()
        logic_thread.stop()
        socket_thread.stop()

        # exit
        app.exit(0)
    try:
        error = app.exec()
        binance_thread.stop()
        logic_thread.stop()
        socket_thread.stop()
        log_fail("User exit", str(sys.exc_info()[1]))
        sys.exit(0)
    except:
        log_fail("Lỗi giao diện", error)
