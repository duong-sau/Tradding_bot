from binance.enums import ORDER_STATUS_CANCELED, ORDER_STATUS_FILLED, ORDER_STATUS_EXPIRED


class OCO:
    def __init__(self, a_order, b_order, destroy_call_back) -> None:
        super().__init__()
        self.a_order = a_order
        self.b_order = b_order
        self.destroy_call_back = destroy_call_back

    def place(self):
        self.a_order.place()
        self.b_order.place()

    def handel(self, event):
        if event['i'] not in self.get_order_id():
            return
        # continue
        if event['X'] == ORDER_STATUS_CANCELED:
            self.destroy_handel(event)
        elif event['X'] == ORDER_STATUS_FILLED or event['X'] == ORDER_STATUS_EXPIRED:
            self.fill_handle(event)

    def fill_handle(self, event):
        self.destroy_call_back()
        if event['i'] in self.a_order.get_order_id():
            self.trigger_a()
        if event['i'] in self.b_order.get_order_id():
            self.trigger_b()

    def destroy_handel(self, event):
        self.destroy_call_back()

    def trigger_a(self):
        self.b_order.cancel()

    def trigger_b(self):
        self.a_order.cancel()

    def get_order_id(self):
        return self.a_order.get_order_id() + self.b_order.get_order_id()
