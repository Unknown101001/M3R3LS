from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import sys

class Game_Widget(QFrame):
    resized = QtCore.pyqtSignal()
    def __init__(self):
        super(QFrame, self).__init__()
        self.resized.connect(self.resizegame)
    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.resized.emit()
        return super(Game_Widget, self).resizeEvent(a0)
    def resizegame(self):
        pass
    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setBrush(QtGui.QColor(0, 0, 100, 120))
        qp.drawRect(-1, -1, self.width()/2, self.height()/2)
        qp.end()

class Score_Widget(QFrame):
    resized = QtCore.pyqtSignal()
    def __init__(self):
        super(QFrame, self).__init__()
        self.resized.connect(self.resizegame)

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.resized.emit()
        return super(Score_Widget, self).resizeEvent(a0)

    def resizegame(self):
        pass


