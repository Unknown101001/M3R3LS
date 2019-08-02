from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow,QWidget
import sys

def window():
    app = QApplication(sys.argv)
    win = QWidget()
    win.setGeometry(0,0,960,640)
    win.setWindowTitle("M3R3LS - Nine Man Morris aka. MÜHLE ")

    win.show()
    sys.exit(app.exec_())

window()