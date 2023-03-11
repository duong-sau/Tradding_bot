import sys
import traceback

from PyQt5.QtWidgets import QApplication
from qt_material import apply_stylesheet

from Binance.BianceThread import CBinanceThread
from Logic.CLogicThread import CLogicThread
from View.MainView import MainWindow
from connection import register_connections

if __name__ == '__main__':
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_yellow.xml')
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
        mainWindow.show()
        binance_thread.set_symbols()

    except Exception:
        # error
        traceback.print_exc()

        # stop
        binance_thread.stop()
        logic_thread.stop()

        # exit
        app.exit(0)
    sys.exit(app.exec_())