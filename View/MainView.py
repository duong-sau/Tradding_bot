from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, QTimer
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QDesktopWidget

from Common.common import MCN, MCNT, MNT, DISTANCE, NORMAL, dlFIBONACCI, \
    dsFIBONACCI, uaFIBONACCI, dDISTANCE
from Common.m_common import m_math_dict
from Common.n_common import n_math_dict
from View.combobox_view import ComboboxView
from View.control_view import ControlView
from View.input_view import InputView
from View.symbol_view import SymbolView


class MainWindow(QMainWindow):
    open_order_signal = pyqtSignal(tuple)
    update_symbol_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.timer = QTimer()
        self.timer.timeout.connect(self.timer_run)
        self.timer.start(1000)

        self.input_view = InputView()
        self.m_textbox = self.input_view.m_textbox
        self.n_textbox = self.input_view.n_textbox
        self.min_textbox = self.input_view.min_textbox
        self.max_textbox = self.input_view.max_textbox

        self.combobox_view = ComboboxView()
        self.m_combobox = self.combobox_view.probability_box
        self.tx_long = self.combobox_view.long_radio

        self.margin_textbox = self.combobox_view.margin_input

        self.control_view = ControlView()
        self.long_button = self.control_view.long_button
        self.short_button = self.control_view.short_button

        self.symbol_view = SymbolView()
        self.mark_price_label = self.symbol_view.mark_label
        self.current_price_label = self.symbol_view.current_label
        self.symbol_select = self.symbol_view.symbol_select

        self.create_view()
        self.create_layout()
        self.setup_connections()

    def create_view(self):
        desktop = QDesktopWidget()
        screen_rect = desktop.screenGeometry()
        self.setGeometry(0, 0, screen_rect.width(), screen_rect.height() - 50)
        self.setWindowTitle('Trading Bot')

    def create_layout(self):
        layout = QGridLayout()
        layout.addWidget(self.input_view, 0, 0, 4, 4)
        layout.addWidget(self.combobox_view, 0, 4, 4, 2)
        layout.addWidget(self.control_view, 8, 0, 1, 4)
        layout.addWidget(self.symbol_view, 8, 4, 1, 2)

        # main widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def setup_connections(self):
        self.long_button.clicked.connect(self.open_long)
        self.short_button.clicked.connect(self.open_short)
        self.symbol_select.currentTextChanged.connect(self.update_symbol)

    @QtCore.pyqtSlot()
    def open_long(self):
        data = self.get_value(), 'BUY'
        self.open_order_signal.emit(data)

    @QtCore.pyqtSlot()
    def open_short(self):
        data = self.get_value(), 'SELL'
        self.open_order_signal.emit(data)

    @QtCore.pyqtSlot(str, str)
    def update_price(self, mark, current):
        self.mark_price_label.setText(mark)
        self.current_price_label.setText(current)

    @QtCore.pyqtSlot(list)
    def set_symbols(self, symbol_names):
        self.symbol_select.addItems(symbol_names)

    @QtCore.pyqtSlot(str)
    def update_symbol(self, symbol):
        self.update_symbol_signal.emit(symbol)

    def timer_run(self):
        self.update_n_max()

    def get_value(self):
        data = {
            'm_list': self.calculator_m(),
            'n_list': self.calculator_n(),
            'symbol': self.symbol_select.currentText(),
            'margin': self.margin_textbox.get_value()
        }
        return data

    def calculator_m(self):
        m_probability = self.get_m_probability()
        m = self.m_textbox.get_value() * self.margin_textbox.get_value()
        n = self.n_textbox.get_value()
        m_list = m_math_dict[m_probability](0, m, n)
        return m_list

    def calculator_n(self):
        n = self.n_textbox.get_value()
        min_val = self.min_textbox.get_value()
        max_val = self.max_textbox.get_value()
        n_probability = self.get_n_probability()
        n_list = n_math_dict[n_probability](min_val, max_val, n)
        return n_list

    def get_n_probability(self):
        probability = self.m_combobox.currentText()
        long = self.tx_long.isChecked()
        if long:

            if probability == MCN:
                m_probability = dDISTANCE
            elif probability == MCNT:
                m_probability = dlFIBONACCI
            elif probability == MNT:
                m_probability = dlFIBONACCI
            else:
                m_probability = ""
        else:

            if probability == MCN:
                m_probability = DISTANCE
            elif probability == MCNT:
                m_probability = dsFIBONACCI
            elif probability == MNT:
                m_probability = dsFIBONACCI
            else:
                m_probability = ""
        return m_probability

    def get_m_probability(self):
        probability = self.m_combobox.currentText()
        if probability == MCN:
            m_probability = uaFIBONACCI
        elif probability == MCNT:
            m_probability = uaFIBONACCI
        elif probability == MNT:
            m_probability = NORMAL
        else:
            m_probability = ""
        return m_probability

    def update_n_max(self):
        try:
            n = self.calculator_n_max()
            self.n_textbox.label.setText(f'Số lệnh (max: {n})')
        except:
            pass

    def calculator_n_max(self):

        margin = self.margin_textbox.get_value()

        m_probability = self.get_m_probability()
        m = self.m_textbox.get_value()

        n_probability = self.get_n_probability()
        min_val = self.min_textbox.get_value()
        max_val = self.max_textbox.get_value()

        for n in range(2, 50, 1):
            n_list = n_math_dict[n_probability](min_val, max_val, n)
            m_list = m_math_dict[m_probability](0, m, n)
            for m_val, n_val in zip(m_list, n_list):

                if round(margin * m_val / n_val, 3) < 0.001:
                    return n - 2

    # def test(self):
    #     try:
    #         self.m_textbox.textbox.setText("10000")
    #         self.n_textbox.textbox.setText('5')
    #         current_price = float(self.price_label.text())
    #         self.min_textbox.textbox.setText(str(current_price - 100))
    #         # self.min_textbox.textbox.setText(str(29000))
    #
    #         self.max_textbox.textbox.setText(str(current_price + 100))
    #         # self.max_textbox.textbox.setText(str(30000))
    #         self.a.textbox.setText('50')
    #         self.stop_loss_textbox.textbox.setText(str(current_price - 200))
    #         self.take_profit1_textbox.textbox.setText(str(current_price + 200))
    #         self.take_profit2_textbox.textbox.setText(str(current_price + 300))
    #         self.margin_textbox.textbox.setText('30')
    #     except:
    #         pass

    def test(self):
        try:
            self.m_textbox.textbox.setText("1000")
            self.n_textbox.textbox.setText('5')
            current_price = float(self.current_price_label.text())
            self.min_textbox.textbox.setText(str(current_price - 100))
            self.max_textbox.textbox.setText(str(current_price + 100))
            self.margin_textbox.textbox.setText('1')
        except:
            pass
