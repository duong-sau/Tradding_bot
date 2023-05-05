from Binance.Strage.OCO import OCO
from Binance.Strage.OTO import OTO


class OTOCO(OTO):
    def __init__(self, limit_order, take_profit_order, stop_loss_order, destroy_call_back) -> None:
        trigger_order = OCO(take_profit_order, stop_loss_order, self.destroy)
        super().__init__(limit_order, trigger_order, self.destroy)
        self.destroy_function = destroy_call_back

    def destroy(self):
        self.destroy_function(self)
