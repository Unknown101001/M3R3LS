from widgets import *
from stone import Stone
from board import Board
from player import Player

class Game:
    def __init__(self, board, player1, player2=None):
        self.commode = True if player2 is None else False
        self.board = board
        self.player1 = player1
        self.player2 = player2
        self.com = None
        self.on_move = 1  # 0-com 1-player1 2-player2
        self.init_Game()
        self.players =[player1]
    def init_Player(self,p,color):
        for i in range(p.n_ia):
            stone = Stone(color)
            p.stones.append(stone)
    def init_Game(self):
        self.init_Player(self.player1,"dunkel")

    def clicked_vert(self, vn, vn_old):
        if self.on_move == 1:
            self.player1.action(self.board, vn)
            if self.player1.status>=2:
                self.player1.end_move()
                print("Move done")
            if self.commode:
                self.on_move = 0
            else: self.on_move = 2
