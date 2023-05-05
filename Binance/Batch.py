from PyQt5.QtCore import QThread

from Binance.OTOListener import OTOListener
from Binance.WebSocket import CSocket


class Batch(QThread):
    def __init__(self, datas) -> None:
        super().__init__()
        self.socket = CSocket(call_back=self.handel, check_destroy=self.check_destroy)
        self.position_list = []
        for data in datas:
            position = OTOListener(data)
            self.position_list.append(position)

    def place_order(self):
        for position in self.position_list:
            position.place_order()

    def handel(self, event):
        print(event)
        pass
    def check_destroy(self):
        pass
