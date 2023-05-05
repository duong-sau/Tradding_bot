import re

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPlainTextEdit, QPushButton

message_format = \
    f'''
Giá thanh lý           L        : %l%

Margin đề xuất         RX       : %rx%
                       PNL      : %pnl%
                       SUM-PNL  : %sumpnl%

----------------------------------------------------------
STOP LOSS     (%) : %sl% %
T___ P__1     (%) : %tp1% %
T___ P__2     (%) : %tp2% %
'''


class PNLView(QWidget):
    def __init__(self, test, parent=None):
        super().__init__(parent)
        self.pnl, self.sum_pnl = 0, 0
        self.L, self.rx, self.sl, self.tp1, self.tp2 = "0", "0", "", "", ""
        self.setWindowTitle("Log Window")

        # Tạo QPlainTextEdit để hiển thị console log
        layout = QVBoxLayout(self)
        self.log_console = QPlainTextEdit(self)
        self.log_console.setReadOnly(True)
        layout.addWidget(self.log_console)

        # Tạo nút "Clear Log" để xóa nội dung trong QPlainTextEdit
        self.clear_button = QPushButton("Test")
        layout.addWidget(self.clear_button)
        self.clear_button.clicked.connect(test)

        # Thiết lập font chữ và cỡ chữ cho QPlainTextEdit
        font = QFont("Consolas", 20)
        self.log_console.setFont(font)

        # Thiết lập màu sắc cho QPlainTextEdit
        stylesheet = """
            QPlainTextEdit {
                background-color: black;
                color: white;
                font-family: Consolas;
                font-size: 10pt;
            }
        """
        self.log_console.setStyleSheet(stylesheet)

    def update(self):
        # Ghi log vào QPlainTextEdit
        self.clear_log()
        message = message_format
        message = re.sub('%l%', self.L, message)
        message = re.sub('%rx%', self.rx, message)
        message = re.sub('%pnl%', str(self.pnl), message)
        message = re.sub('%sumpnl%', str(self.sum_pnl), message)
        message = re.sub('%sl%', self.sl, message)
        message = re.sub('%tp1%', self.tp1, message)
        message = re.sub('%tp2%', self.tp2, message)
        self.log_console.insertPlainText(message)

    def clear_log(self):
        # Xóa nội dung trong QPlainTextEdit
        self.log_console.clear()

    def update_pnl(self, pnl, sum_pnl):
        self.pnl = pnl
        self.sum_pnl = sum_pnl
        self.update()

    def set_text(self, sl, tp1, tp2):
        self.sl, self.tp1, self.tp2 = str(round(sl, 3)), str(round(tp1, 3)), str(round(tp2, 3))
        self.update()

    def log_cant_cal(self):
        self.clear_log()
        self.log_console.insertPlainText("Chưa tính được")
