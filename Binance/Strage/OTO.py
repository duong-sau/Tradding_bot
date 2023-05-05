from binance.enums import ORDER_STATUS_CANCELED, ORDER_STATUS_FILLED, ORDER_STATUS_EXPIRED


class OTO:
    def __init__(self, base_order, trigger_order, destroy_call_back) -> None:
        super().__init__()
        self.base_order = base_order
        self.trigger_order = trigger_order
        self.destroy_call_back = destroy_call_back

    def place(self):
        self.base_order.place()

    def handel(self, event):
        if event['i'] not in self.get_order_id():
            return
        # continue
        if event['X'] == ORDER_STATUS_CANCELED:
            self.destroy_handel(event)
        elif event['X'] == ORDER_STATUS_FILLED or event['X'] == ORDER_STATUS_EXPIRED:
            self.fill_handle(event)

    def fill_handle(self, event):
        if event['i'] in self.base_order.get_order_id():
            self.trigger_base_order()
        if event['i'] in self.trigger_order.get_order_id():
            self.trigger_order.handel(event)

    def destroy_handel(self, event):
        self.destroy_call_back()

    def trigger_base_order(self):
        self.trigger_order.place()

    def get_order_id(self):
        return self.base_order.get_order_id() + self.trigger_order.get_order_id()

    def cancel(self):
        self.base_order.cancel()
