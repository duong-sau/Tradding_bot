from Binance.Strage.OTO import OTO


class OTOCOHalf(OTO):

    def __init__(self,
                 limit_parameter, take1_parameter, stop1_parameter, take2_parameter, stop2_parameter) -> None:
        super().__init__(limit_parameter, take1_parameter, stop1_parameter, take2_parameter, stop2_parameter)

    def make_step2(self):
        return

    def step2_trigger(self):
        return
