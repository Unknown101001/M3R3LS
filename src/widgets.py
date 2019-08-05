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

    def __init__(self, game):
        super(QFrame, self).__init__()
        self.game = game
        self.initUI()
        self.resized.connect(self.resizegame)

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
        vimg = QImage("img/board.jpg")
        self.verteximg = vimg.scaled(QSize(self.vertex_size, self.vertex_size))
        self.vertpixmap = QPixmap().fromImage(self.verteximg)
        self.vertex_labels = []
        for vertex in self.vertices:
            label = QLabel(self)
            #label.resize(self.vertex_size, self.vertex_size)
            label.setPixmap(self.vertpixmap)
            label.move(vertex[0], vertex[1])
            label.setAttribute(Qt.WA_TranslucentBackground)
            self.vertex_labels.append(label)

    def paintEvent(self, e):
        def draw_line(v1, v2):
            linewidth = int(self.vertex_size/2)
            horizontal = True if v1[1] == v2[1] else False
            qp = QtGui.QPainter()
            qp.begin(self)
            qp.setBrush(QtGui.QColor(43, 29, 14, 120))
            if horizontal:
                qp.drawRect(v1[0] + self.vertex_size, v1[1] + int(self.vertex_size / 4), v2[0]-v1[0]-self.vertex_size,
                            linewidth)
            else:
                qp.drawRect(v1[0]+int(self.vertex_size / 4),v1[1] + self.vertex_size,linewidth,
                            v2[1] - v1[1] - self.vertex_size)
            qp.end()

        for i in range(len(self.adj_mat[0,:])):
            for j in range(len(self.adj_mat[0,:])):

                if self.adj_mat[i,j] == 1:
                    l = min([i, j])
                    k = max([i, j])
                    draw_line(self.vertices[l],self.vertices[k])
    def mousePressEvent(self, e):
        pass



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
        vimg = QImage("img/Vertex.png")
        self.verteximg = vimg.scaled(QSize(20, 20))
        self.vertpixmap = QPixmap().fromImage(self.verteximg)
        for vertexlabel in self.vertex_labels:
            vertex = self.vertices[self.vertex_labels.index(vertexlabel)]
            vertexlabel.move(vertex[0], vertex[1])


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
