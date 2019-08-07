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
        if player2 is None:
            self.players =[player1]
        else:
            self.players = [player1,player2]
        self.init_Game()
    def init_Player(self,p,color):
        for i in range(p.n_ia):
            stone = Stone(color)
            p.inaktiv_stones.append(stone)
    def init_Game(self):
        colors = ["dunkel","hell"]
        i = 0
        for p in self.players:
            self.init_Player(p,colors[i])
            i += 1

    def clicked_vert(self, vn, vn_old):
        if vn is None:
            print("Wrong click")
        else:
            if self.on_move == 1:
                self.player1.action(self.board, vn)
                if self.player1.status>=2:
                    self.player1.end_move()
                    print("Move done")
                    print()
                if self.commode:
                    self.on_move = 0
                else: self.on_move = 2
            elif self.on_move == 2:
                self.player2.action(self.board, vn)
                if self.player2.status >= 2:
                    self.player2.end_move()
                    print("Move done")
                if self.commode:
                    self.on_move = 0
                else:
                    self.on_move = 1

