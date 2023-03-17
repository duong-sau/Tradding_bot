from PyQt6 import uic
from PyQt6.QtWidgets import QApplication
from qt_material import apply_stylesheet

from View.Style import style

Form, Window = uic.loadUiType("main_view.ui")

app = QApplication([])
apply_stylesheet(app, theme='dark_yellow.xml')


window = Window()
window.setStyleSheet(style)

form = Form()
form.setupUi(window)


window.show()
app.exec()
