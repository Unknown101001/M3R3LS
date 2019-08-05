from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Overlay(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setPalette(QtGui.QPalette(QtCore.Qt.transparent))
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setBrush(QtGui.QColor(255, 255, 255, 80))
        qp.drawRect(-1, -1, self.width(), self.height())
        qp.end()
class PicButton(QAbstractButton):
    def __init__(self, pixmap, parent=None):
        super(PicButton, self).__init__(parent)
        self.pixmap = pixmap

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), self.pixmap)

    def sizeHint(self):
        return self.pixmap.size()


class Game_Widget(QFrame):
    resized = QtCore.pyqtSignal()
    def __init__(self,game):
        super(QFrame, self).__init__()
        self.initUI()
        self.resized.connect(self.resizegame)
    def initUI(self):
        """
        background
        """
        self.overlay = Overlay(self)
        self.overlay.resize(self.width() + 1, self.height() + 1)
        """
        gamefield
        """
        gameheight = self.height() - 60
        h = int(gameheight/6)
        gamewidth = self.width() - 60
        w = int(gamewidth/6)
        """
        vertices
        """
        




    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.resized.emit()
        return super(Game_Widget, self).resizeEvent(a0)
    def resizegame(self):
        gameheight = self.height() - 60
        h = int(gameheight / 6)
        gamewidth = self.width() - 60
        w = int(gamewidth / 6)
        self.overlay.resize(self.width() + 1, self.height() + 1)
        self.v0.move(30,30)
        self.v1.move(int(self.width() / 2)-20, 30)
        self.v2.move(self.width() - 70, 30)
        self.v3.move(30 + w, 30 + h)
        self.v4.move(int(self.width() / 2)-20, 30 + h)
        self.v5.move(self.width() - 70 - w, 30 + h)
        self.v6.move(30 + 2 * w, 30 + 2 * h)
        self.v7.move(int(self.width() / 2)-20, 30 + 2 * h)
        self.v8.move(self.width() - 70 - 2 * w, 30 + 2 * h)



class Score_Widget(QFrame):
    resized = QtCore.pyqtSignal()
    def __init__(self):
        super(QFrame, self).__init__()
        self.initUI()
        self.resized.connect(self.resizegame)
        self.setMinimumHeight(200)
        self.setMaximumWidth(300)

    def initUI(self):
        self.overlay = Overlay(self)
        self.overlay.resize(self.width() + 1, self.height() + 1)

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.resized.emit()
        return super(Score_Widget, self).resizeEvent(a0)

    def resizegame(self):
        self.overlay.resize(self.width() + 1, self.height() + 1)


