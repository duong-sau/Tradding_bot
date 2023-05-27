import sys

from PyQt5.QtWidgets import QApplication
from qt_material import apply_stylesheet

from Binance.BianceThread import CBinanceThread
from Binance.Websocket.WebSocketThread import CSocketThread
from Logic.CLogicThread import CLogicThread
from Telegram.TelegramThread import log_error, error_notification, all_log
from View.MainView import MainWindow
from connection import register_connections


def handle_exception(exc_type, exc_value, exc_traceback):
    try:
        error_notification(f"{exc_type}\n{exc_value}\n{exc_traceback}")
        log_error()
    except:
        all_log()


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

    except Exception:
        log_error()

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
        error_notification(error)
        sys.exit(0)
    except:
        log_error()
        sys.exit(0)
