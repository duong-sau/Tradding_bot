import logging
import re

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPlainTextEdit, QPushButton
from PyQt5.QtGui import QFont

message_format = \
    f'''
Giá thanh lý           LONG     : %long%
                       SHORT    : %short%

Margin đề xuất         RX       : %rx%
                       PNL      : %pnl%

----------------------------------------------------------
STOP LOSS     (%) : %sl%
T___ P__1     (%) : %tp1%
T___ P__2     (%) : %tp2%
'''


class PNLView(QWidget):
    def __init__(self, test, parent=None):
        super().__init__(parent)
        self.long, self.short, self.rx, self.sl, self.tp1, self.tp2, self.pnl = "", "", "", "", "", "", 0
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
        message = message_format
        message = re.sub('%long%', self.long, message)
        message = re.sub('%short%', self.short, message)
        message = re.sub('%rx%', self.rx, message)
        message = re.sub('%pnl%', str(self.pnl), message)
        message = re.sub('%sl%', self.sl, message)
        message = re.sub('%tp1%', self.tp1, message)
        message = re.sub('%tp2%', self.tp2, message)
        self.log_console.insertPlainText(message)

    def clear_log(self):
        # Xóa nội dung trong QPlainTextEdit
        self.log_console.clear()

    def update_pnl(self, pnl):
        self.pnl = pnl
        self.update()

    def set_text(self, long, short, rx, sl, tp1, tp2):
        self.clear_log()
        self.long, self.short, self.rx, self.sl, self.tp1, self.tp2 = str(long), str(short), str(rx), str(sl), str(tp1), str(tp2)
        self.update()

    def log_cant_cal(self):
        self.clear_log()
        self.log_console.insertPlainText("Chưa tính được")
