from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import sys


class PicButton(QAbstractButton):
    def __init__(self, pixmap, parent=None):
        super(PicButton, self).__init__(parent)
        self.pixmap = pixmap

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), self.pixmap)

    def sizeHint(self):
        return self.pixmap.size()


class MainWindow(QMainWindow):
    resized = QtCore.pyqtSignal()

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(0, 0, 960, 640)
        self.setWindowTitle("M3R3LS - Nine Man Morris aka. MÜHLE ")
        self.initUI()
        self.resized.connect(self.resizedwin)

    def resizeEvent(self, event):
        self.resized.emit()
        return super(MainWindow, self).resizeEvent(event)

    def initUI(self):
        """
        background
        """
        self.img = QImage("img/background.png")
        self.simg = self.img.scaled(QSize(self.width(), self.height()))
        palette = QPalette()
        palette.setBrush(10, QBrush(self.simg))
        self.setPalette(palette)

        """
        menu
        """
        self.menushown = True
        self.menu = PicButton(QPixmap("img/menu.png"),self)
        self.menu.resize(32,32)
        self.menu.clicked.connect(self.menu_pressed)
        self.menu.move(self.width()-40,8)

        self.b_newgame = PicButton(QPixmap("img/button_new-game.png"),self)
        self.b_newgame.resize(160,40)
        self.b_newgame.clicked.connect(self.newgame)
        self.b_newgame.move(self.width() / 2 - 80, self.height() / 2 -50)

        self.b_quitgame = PicButton(QPixmap("img/button_quit-game.png"), self)
        self.b_quitgame.resize(160, 40)
        self.b_quitgame.clicked.connect(self.quitgame)
        self.b_quitgame.move(self.width()/2 - 80, self.height()/2+10)

        self.whichgame = False
        g = abs(min([100, self.width() / 2 - 60]))

        self.b_player = PicButton(QPixmap("img/hoodie.png"),self)
        self.b_player.resize(g,g)
        self.b_player.clicked.connect(self.start_playergame)
        self.b_player.move(self.width()/2 - g -20,self.height()/2)
        self.b_player.hide()

        self.b_com = PicButton(QPixmap("img/processor.png"), self)
        self.b_com.resize(g, g)
        self.b_com.clicked.connect(self.start_comgame)
        self.b_com.move(self.width()/2 + 20,self.height()/2)
        self.b_com.hide()

    """
        styles
        """
    def start_playergame(self):
        pass
    def start_comgame(self):
        pass
    def newgame(self):
        print("new")
        self.hide_menu()
        self.whichgame = True
        self.b_com.show()
        self.b_player.show()
    def quitgame(self):
        self.close()

    def show_menu(self):
        self.menushown = True
        self.b_newgame.show()
        self.b_quitgame.show()
        print("appear")

    def hide_menu(self):
        self.b_quitgame.hide()
        self.b_newgame.hide()
        self.menushown = False
        print("disappear")
    def resizedwin(self):
        self.simg = self.img.scaled(QSize(self.width(), self.height()))
        palette = QPalette()
        palette.setBrush(10, QBrush(self.simg))
        self.setPalette(palette)
        self.menu.move(self.width() - 40, 8)
        if self.menushown:
            self.b_newgame.move(self.width() / 2 - 80, self.height() / 2 - 50)
            self.b_quitgame.move(self.width() / 2 - 80, self.height() / 2 + 10)
        if self.whichgame:
            g = abs(min([160, self.width() / 2 - 60]))
            self.b_player.resize(g, g)
            self.b_player.move(self.width() - g - 20, self.height())
            self.b_com.resize(g, g)
            self.b_com.move(self.width() + 20, self.height())


    def menu_pressed(self):
        if self.menushown:
            self.hide_menu()
            self.menushown = False
        else:
            self.show_menu()
            self.menushown = True


def window():
    app = QApplication(sys.argv)
    win = MainWindow()

    win.show()
    sys.exit(app.exec_())


window()
