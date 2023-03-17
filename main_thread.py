from PyQt5.QtWidgets import QApplication, QMainWindow
from qt_material import apply_stylesheet

from Control import Control
from Data import Data
from View.Style import style
from main_view import Ui_main_view


window = QMainWindow()

app = QApplication([])
apply_stylesheet(app, theme='dark_yellow.xml')

window.setStyleSheet(style)

form = Ui_main_view()
form.setupUi(window)

data = Data(form)
control = Control(form)

window.show()
app.exec()
