import sys

from binance.exceptions import BinanceRequestException, BinanceAPIException

from Binance.Common import get_stop_loss_form_limit, CANCELED, FILLED
from Binance.Strage.OTOCOFull import OTOCOFull
from Binance.Strage.OTOCOHalf import OTOCOHalf
from View.a_common.MsgBox import msg_box


class OTOControl:

    def __init__(self, client, destroy_call_back, parameter, stop_loss, full_type) -> None:
        super().__init__()

        limit_parameter = parameter
        stop_loss1_parameter = get_stop_loss_form_limit(limit_order=limit_parameter, stop_loss=stop_loss)

        if full_type:
            self.OTOCO = OTOCOFull(client=client, limit_parameter=limit_parameter, stop_parameter=stop_loss1_parameter)
        else:
            self.OTOCO = OTOCOHalf(client=client, limit_parameter=limit_parameter, stop_parameter=stop_loss1_parameter)

        self.destroy_call_back = destroy_call_back

        self.OTOCO.place()
        return

    def get_order_id(self):
        return self.OTOCO.get_order_id()

    # ################HANDEL##################
    def handle(self, event):
        try:
            if event['i'] not in self.get_order_id():
                return
            # continue
            if event['X'] == CANCELED:
                self.destroy_handel()
            elif event['X'] == FILLED:
                self.fill_handle(event)
            # error

        except (BinanceAPIException, BinanceRequestException):
            msg_box(sys.exc_info()[1])

    def fill_handle(self, event):
        self.OTOCO.handel(event)

    def destroy_handel(self):
        self.destroy_call_back(self)
