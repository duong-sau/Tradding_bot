from Binance.PositionBatch import PositionBatch


class PositionControl:
    def __init__(self):
        self.position_batch = []
        pass

    def add_batch(self, datas):
        position = PositionBatch(datas)
        self.position_batch.append(position)
        position.place()

    def handel(self, event):
        for position in self.position_batch:
            position.handel(event)
