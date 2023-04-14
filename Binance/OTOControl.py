import sys

from binance.exceptions import BinanceRequestException, BinanceAPIException

from Binance.Common import get_stop_loss_form_limit, get_take_profit_form_limit, CANCELED, FILL
from Binance.Strage.OTOCOFull import OTOCOFull
from Binance.Strage.OTOCOHalf import OTOCOHalf
from View.a_common.MsgBox import msg_box

fill_limit = 'fill_limit'
fill_stop1 = 'fill_stop1'
fill_stop2 = 'fill_stop2'
fill_take1 = 'fill_take1'
fill_take2 = 'fill_take2'
cancel_by_client = 'cbl'
cancel_by_system = 'cbs'


def destroy_handel(event):
    print(event)
    pass


class OTOControl:

    def __init__(self, destroy_call_back, cancel_call_back,
                 parameter,
                 stop_loss1, take_profit1, a_quantity,
                 stop_loss2, take_profit2, b_quantity) -> None:
        super().__init__()

        limit_parameter = parameter
        stop_loss1_parameter = get_stop_loss_form_limit(limit_order=limit_parameter,
                                                        stop_loss=stop_loss1,
                                                        quantity=a_quantity)
        take_profit1_parameter = get_take_profit_form_limit(limit_order=limit_parameter,
                                                            take_profit=take_profit1,
                                                            quantity=a_quantity)

        stop_loss2_parameter = get_stop_loss_form_limit(limit_order=limit_parameter,
                                                        stop_loss=stop_loss2,
                                                        quantity=b_quantity)
        take_profit2_parameter = get_take_profit_form_limit(limit_order=limit_parameter,
                                                            take_profit=take_profit2,
                                                            quantity=b_quantity)

        if b_quantity >= 0.001:

            self.OTOCO = OTOCOFull(limit_parameter=limit_parameter,
                                   take1_parameter=take_profit1_parameter,
                                   stop1_parameter=stop_loss1_parameter,
                                   take2_parameter=take_profit2_parameter,
                                   stop2_parameter=stop_loss2_parameter)
        else:
            self.OTOCO = OTOCOHalf(limit_parameter=limit_parameter,
                                   take1_parameter=take_profit1_parameter,
                                   stop1_parameter=stop_loss1_parameter,
                                   take2_parameter=take_profit2_parameter,
                                   stop2_parameter=stop_loss2_parameter)

        self.destroy_call_back = destroy_call_back
        self.cancel_all_call_back = cancel_call_back

        self.OTOCO.place()
        return

    def get_order_id(self):
        return self.OTOCO.get_order_id()

    def handle(self, event):
        try:
            if event['i'] not in self.get_order_id():
                return

            # continue
            if event['X'] == CANCELED:
                destroy_handel(event)
            elif event['X'] == FILL:
                self.fill_handle(event)
            # error

        except (BinanceAPIException, BinanceRequestException):
            msg_box(sys.exc_info()[1])

    def fill_handle(self, event):
        self.OTOCO.handel(event)
