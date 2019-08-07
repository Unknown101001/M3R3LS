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
        qp.setBrush(QtGui.QColor(255, 255, 255, 0))
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
    clicked_vert = QtCore.pyqtSignal()
    last_clicked_vert = -1
    last_last_clicked_vert = -1

    def __init__(self, game):
        super(QFrame, self).__init__()
        self.game = game
        self.initUI()
        self.resized.connect(self.resizegame)
        self.clicked_vert.connect(self.game_clicked_vert)

    def initUI(self):
        """
        layout
        """
        """
        background
        """
        self.overlay = Overlay(self)
        self.overlay.resize(self.width() + 1, self.height() + 1)
        """
        gamefield
        """
        self.side_spacing = 30
        self.vert_spacing = 30
        self.vertex_size = 40
        self.cr = - int(self.vertex_size / 2)
        gameheight = self.height() - 2 * self.vert_spacing
        gamewidth = self.width() - 2 * self.side_spacing

        unscaled_vertices = self.game.board.vertices
        self.adj_mat = self.game.board.adjazenz_matrix
        min_x = min([tup.x for tup in unscaled_vertices])
        max_x = max([tup.x for tup in unscaled_vertices])
        max_y = max([tup.y for tup in unscaled_vertices])
        min_y = min([tup.y for tup in unscaled_vertices])

        def scale(v):
            tmp = (int(v[0] * gamewidth / (max_x - min_x)), int(v[1] * gameheight / (max_y - min_y)))
            tmp = (tmp[0] + self.side_spacing + self.cr, tmp[1] + self.vert_spacing + self.cr)
            return tmp

        self.vertices = [scale((v.x, v.y)) for v in unscaled_vertices]

        yimg = QImage("img/hell.png")
        bimg = QImage("img/dunkel.png")
        syimg = QPixmap().fromImage(yimg.scaled(QSize(self.vertex_size, self.vertex_size)))
        sbimg = QPixmap().fromImage(bimg.scaled(QSize(self.vertex_size, self.vertex_size)))
        self.stone_img = {"hell": syimg, "dunkel": sbimg}

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setBrush(QtGui.QColor(255, 255, 255, 80))
        qp.drawRect(-1, -1, self.width(), self.height())
        qp.end()

        def draw_line(v1, v2):
            linewidth = int(self.vertex_size / 2)
            horizontal = True if v1[1] == v2[1] else False
            qp = QtGui.QPainter()
            qp.begin(self)
            qp.setBrush(QtGui.QColor(43, 29, 14, 120))
            if horizontal:
                qp.drawRect(v1[0] + self.vertex_size, v1[1] + int(self.vertex_size / 4),
                            v2[0] - v1[0] - self.vertex_size,
                            linewidth)
            else:
                qp.drawRect(v1[0] + int(self.vertex_size / 4), v1[1] + self.vertex_size, linewidth,
                            v2[1] - v1[1] - self.vertex_size)
            qp.end()


        def draw_vert(v):
            qp = QtGui.QPainter()
            qp.begin(self)
            qp.setBrush(QtGui.QColor(43, 29, 14, 120))
            qp.drawRect(v[0]
                        ,v[1],
                        self.vertex_size,self.vertex_size)
            qp.end()


        for i in range(len(self.adj_mat[0, :])):
            for j in range(len(self.adj_mat[0, :])):

                if self.adj_mat[i, j] == 1:
                    l = min([i, j])
                    k = max([i, j])
                    draw_line(self.vertices[l], self.vertices[k])
        for v in self.vertices:
            draw_vert(v)

        for player in self.game.players:
            for stone in player.aktiv_stones:
                if stone.aktiv:
                    vn = stone.vert
                    sx = self.vertices[vn][0]
                    sy = self.vertices[vn][1]


                    #qp = QtGui.QPainter(self)
                    qp.begin(self)
                    rec = QRect(sx-5,sy-5,50,50)
                    qp.drawPixmap(rec,self.stone_img[stone.color])
                    qp.end()


    def get_vertexnum_from_offset(self, offset):
        ox = offset.x()
        oy = offset.y()
        for vert in self.vertices:
            if vert[0] <= ox <= vert[0] + self.vertex_size and vert[1] <= oy <= vert[1] + self.vertex_size:
                return (self.vertices.index(vert))
        return (None)

    def mousePressEvent(self, event):
        super(QFrame, self).mousePressEvent(event)
        self.offset = event.pos()
        self.last_last_clicked_vert = self.last_clicked_vert
        self.last_clicked_vert = self.get_vertexnum_from_offset(self.offset)
        self.clicked_vert.emit()

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.resized.emit()
        return super(Game_Widget, self).resizeEvent(a0)

    def resizegame(self):
        self.overlay.resize(self.width() + 1, self.height() + 1)

        gameheight = self.height() - 2 * self.vert_spacing
        gamewidth = self.width() - 2 * self.side_spacing

        unscaled_vertices = self.game.board.vertices
        adj_mat = self.game.board.adjazenz_matrix
        min_x = min([tup.x for tup in unscaled_vertices])
        max_x = max([tup.x for tup in unscaled_vertices])
        max_y = max([tup.y for tup in unscaled_vertices])
        min_y = min([tup.y for tup in unscaled_vertices])

        def scale(v):
            tmp = (int(v[0] * gamewidth / (max_x - min_x)), int(v[1] * gameheight / (max_y - min_y)))
            tmp = (tmp[0] + self.side_spacing + self.cr, tmp[1] + self.vert_spacing + self.cr)
            return tmp

        self.vertices = [scale((v.x, v.y)) for v in unscaled_vertices]


    def game_clicked_vert(self):
        self.game.clicked_vert(self.last_clicked_vert, self.last_last_clicked_vert)
        self.update()


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
