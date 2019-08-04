from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import sys

class Game_Widget(QFrame):
    resized = QtCore.pyqtSignal()
    def __init__(self):
        super(QFrame, self).__init__()
        self.initUI()
        self.resized.connect(self.resizegame)
    def initUI(self):
        """
        styles
        """
        self.setStyleSheet("background-image: url(img/board.jpg)")
        """
        background
        """
        self.img = QImage("img/board.jpg")
        self.simg = self.img.scaled(QSize(self.width(), self.height()))
        palette = QPalette()
        palette.setBrush(10, QBrush(self.simg))
        self.setPalette(palette)
    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.resized.emit()
        return super(Game_Widget, self).resizeEvent(a0)
    def resizegame(self):
        self.simg = self.img.scaled(QSize(self.width(), self.height()))
        palette = QPalette()
        palette.setBrush(10, QBrush(self.simg))
        self.setPalette(palette)


class Score_Widget(QFrame):
    resized = QtCore.pyqtSignal()
    def __init__(self):
        super(QFrame, self).__init__()
        self.initUI()
        self.resized.connect(self.resizegame)

    def initUI(self):
        """
        styles
        """
        self.setStyleSheet("background-image: url(img/board.jpg)")
        """
        background
        """
        self.img = QImage("img/board.jpg")
        self.simg = self.img.scaled(QSize(self.width(), self.height()))
        palette = QPalette()
        palette.setBrush(10, QBrush(self.simg))
        self.setPalette(palette)
        self.setMaximumWidth(int(self.height()/2))

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.resized.emit()
        return super(Score_Widget, self).resizeEvent(a0)

    def resizegame(self):
        pass


