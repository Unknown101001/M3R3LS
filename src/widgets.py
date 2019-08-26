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
                        , v[1],
                        self.vertex_size, self.vertex_size)
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
            for stone in player.activ_stones:
                if stone.activ:
                    vn = stone.vert
                    sx = self.vertices[vn][0]
                    sy = self.vertices[vn][1]

                    # qp = QtGui.QPainter(self)
                    qp.begin(self)
                    rec = QRect(sx - 5, sy - 5, 50, 50)
                    qp.drawPixmap(rec, self.stone_img[stone.color])
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


class Score_Widget(QWidget):

    def __init__(self, game):
        super(QWidget, self).__init__()
        self.setMinimumHeight(200)
        self.setMaximumWidth(300)
        self.game = game
        self.frame1 = Player_Frame("name", game, self.game.player1)
        self.frame2 = Player_Frame("name", game, self.game.player2)
        self.initUI()

    def initUI(self):
        layout = QGridLayout()
        layout.addWidget(self.frame1,0,0)
        layout.addWidget(self.frame2,1,0)
        layout.setHorizontalSpacing(10)
        self.setLayout(layout)
    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setBrush(QtGui.QColor(255, 255, 255, 80))
        qp.drawRect(-1, -1, self.width(), self.height())
        qp.end()

    def update(self):
        self.frame1.update()
        self.frame2.update()




class Player_Frame(QFrame):
    resized = QtCore.pyqtSignal()

    def __init__(self, name, game, player):
        super(QFrame, self).__init__()
        self.name = name
        self.game = game
        self.player = player
        self.resized.connect(self.resizeframe)
        self.color = self.player.inactiv_stones[0].color
        self.initUI()

    def initUI(self):
        '''
        layout
        '''
        self.verticalLayoutWidget = QtWidgets.QWidget(self)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(9, 10, 381, 281))
        self.verticalLayoutWidget.setAttribute(Qt.WA_TranslucentBackground)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        '''
        stonelabel 
        '''
        self.stonesize = int(self.height()/8)
        self.yimg = QImage("img/hell.png")
        self.bimg = QImage("img/dunkel.png")
        syimg = QPixmap().fromImage(self.yimg.scaled(QSize(self.stonesize, self.stonesize)))
        sbimg = QPixmap().fromImage(self.bimg.scaled(QSize(self.stonesize, self.stonesize)))
        self.stone_img = {"hell": syimg, "dunkel": sbimg}
        self.stonelabel = QLabel(self.verticalLayoutWidget)
        self.stonelabel.setPixmap(self.stone_img[self.color])
        self.stonelabel.setAttribute(Qt.WA_TranslucentBackground)
        self.stonelabel.setAlignment(QtCore.Qt.AlignCenter)

        '''
        grid
        '''
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")


        '''
        labels in grid
        '''
        self.phase = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.phase.setAlignment(QtCore.Qt.AlignCenter)
        self.phase.setObjectName("phase")
        self.phase.setAttribute(Qt.WA_TranslucentBackground)
        self.gridLayout.addWidget(self.phase, 0, 0, 1, 1)

        self.phase_instruction = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.phase_instruction.setAlignment(QtCore.Qt.AlignCenter)
        self.phase_instruction.setObjectName("phase_instruction")
        self.phase_instruction.setAttribute(Qt.WA_TranslucentBackground)
        self.gridLayout.addWidget(self.phase_instruction, 0, 1, 1, 1)


        self.inactiv_stones_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.inactiv_stones_label.setAlignment(QtCore.Qt.AlignCenter)
        self.inactiv_stones_label.setObjectName("inactiv_stones_label")
        self.inactiv_stones_label.setAttribute(Qt.WA_TranslucentBackground)
        self.gridLayout.addWidget(self.inactiv_stones_label, 1, 1, 1, 1)

        self.activ_stones_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.activ_stones_label.setAlignment(QtCore.Qt.AlignCenter)
        self.activ_stones_label.setObjectName("activ_stones_label")
        self.activ_stones_label.setAttribute(Qt.WA_TranslucentBackground)
        self.gridLayout.addWidget(self.activ_stones_label, 2, 1, 1, 1)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_2.setText("Stones in ")
        self.label_2.setAttribute(Qt.WA_TranslucentBackground)
        self.horizontalLayout.addWidget(self.label_2)
        self.pocket_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.pocket_label.setAlignment(QtCore.Qt.AlignCenter)
        self.pocket_label.setObjectName("pocket_label")
        self.pocket_label.setAttribute(Qt.WA_TranslucentBackground)
        self.horizontalLayout.addWidget(self.pocket_label)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.label_4.setText("Stones on ")
        self.label_4.setAttribute(Qt.WA_TranslucentBackground)
        self.horizontalLayout_2.addWidget(self.label_4)
        self.field_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.field_label.setAlignment(QtCore.Qt.AlignCenter)
        self.field_label.setObjectName("field_label")
        self.field_label.setAttribute(Qt.WA_TranslucentBackground)
        self.horizontalLayout_2.addWidget(self.field_label)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)


        '''
        vertical Layout
        '''
        self.verticalLayout.addWidget(self.stonelabel)
        self.verticalLayout.addLayout(self.gridLayout)



        _layout = QVBoxLayout()
        _layout.setAlignment(Qt.AlignCenter)
        _layout.addWidget(self.verticalLayoutWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalPolicy(0)
        sizePolicy.setVerticalStretch(0)
        self.verticalLayoutWidget.setSizePolicy(sizePolicy)
        self.setLayout(_layout)



    def paintEvent(self, e):
        if self.player.opp.status==2:
            qp = QtGui.QPainter()
            qp.begin(self)
            qp.setBrush(QtGui.QColor(255, 255, 0, 120))
            qp.drawRect(-1, -1, 11, self.height())
            qp.drawRect(-1, -1, self.width(), 10)
            qp.drawRect(self.width()-10,-1,10,self.height())
            qp.drawRect(-1,self.height()-10,self.width(),10)
            qp.end()


    def update(self):
        print("Update")
        self.inactiv_stones_label.setText(str(len(self.game.player1.inactiv_stones)))
        self.activ_stones_label.setText(str(len(self.player.activ_stones)))
        self.repaint()






    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.resized.emit()
        return super(Player_Frame, self).resizeEvent(a0)

    def resizeframe(self):
        self.stonesize = int(self.height() / 8)
        syimg = QPixmap().fromImage(self.yimg.scaled(QSize(self.stonesize, self.stonesize)))
        sbimg = QPixmap().fromImage(self.bimg.scaled(QSize(self.stonesize, self.stonesize)))
        self.stone_img = {"hell": syimg, "dunkel": sbimg}
        self.stonelabel = QLabel()
        self.stonelabel.setPixmap(self.stone_img[self.color])
