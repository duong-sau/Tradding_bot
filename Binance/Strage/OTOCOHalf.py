from Binance.Strage.OTO import OTO


class OTOCOHalf(OTO):

    def __init__(self, client, limit_parameter, stop_parameter) -> None:
        super().__init__(client, limit_parameter, stop_parameter)

    def make_stop_loss(self):
        return
