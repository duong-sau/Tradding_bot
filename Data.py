class Data:
    def __init__(self, ui) -> None:
        super().__init__()
        self.ui = ui

    def get_data(self):
        data = {
            'budget': self.get_budget_data(),
            'order': self.get_order_data(),
            'stop_loss_take_profit': self.get_stop_loss_take_profit()
        }
        return data

    def get_order_data(self):
        ui = self.ui
        order_data = {
            'n': ui.n_input.text(),
            'allocator': ui.n_allocator_input.text(),
            'min_max': self.get_min_max()
        }
        return order_data

    def get_budget_data(self):
        ui = self.ui
        budget_data = {
            'm': ui.m_input.text(),
            'allocator': ui.m_allocator.text()
        }
        return budget_data

    def get_min_max(self):
        ui = self.ui
        min_max = {
            'min_val': ui.min_val_input.text(),
            'max_val': ui.max_val_input.text()
        }
        return min_max

    def get_stop_loss_take_profit(self):
        ui = self.ui
        stop_loss_take_profit = {
            'stop_loss': ui.stop_loss_input.text(),
            'take_profit_1': ui.take_profit_1_price_input.text(),
            'take_profit_2': ui.take_profit_2_price_input.text()
        }
        return stop_loss_take_profit
