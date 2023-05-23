import time

from PyQt5 import QtCore
from PyQt5.QtCore import QThread, pyqtSignal

from Logic.ProcessData import process


class CLogicThread(QThread):
    open_order_signal = pyqtSignal(list)
    update_price_signal = pyqtSignal(str, str)

    def __init__(self, parent=None):
        super(CLogicThread, self).__init__(parent)
        self.running = True

    def run(self):
        while self.running:
            time.sleep(1)

    def stop(self):
        self.running = False

    @QtCore.pyqtSlot(tuple)
    def open_order(self, data):
        valid, data = process(data)
        if not valid:
            return
        self.open_order_signal.emit(data)

