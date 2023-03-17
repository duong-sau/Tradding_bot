class Control:
    def __init__(self, ui) -> None:
        super().__init__()
        self.ui = ui

    def update_price(self, price):
        self.ui.price_display.settText(price)
