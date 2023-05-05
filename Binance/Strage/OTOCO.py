from Binance.Strage.OCO import OCO
from Binance.Strage.OTO import OTO


class OTOCO(OTO):
    def __init__(self, limit_order, take_profit_order, stop_loss_order, destroy_call_back, finish_call_back) -> None:
        trigger_order = OCO(take_profit_order, stop_loss_order, self.finish)
        super().__init__(limit_order, trigger_order, self.destroy)
        self.destroy_function = destroy_call_back
        self.finish_function = finish_call_back

    def destroy(self):
        self.destroy_function(self)

    def finish(self):
        self.finish_function()
