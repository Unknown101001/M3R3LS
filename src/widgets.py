from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import sys

class Game_Widget(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        self.resized.connect(self.resizegame)
    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.resized.emit()
        return super(QWidget, self).resizeEvent(a0)
    def resizegame(self):
        pass

class Score_Widget(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        self.resized.connect(self.resizegame)

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.resized.emit()
        return super(QWidget, self).resizeEvent(a0)

    def resizegame(self):
        pass


