from widgets import *
from stone import Stone
from board import Board
from player import Player
import sys
import time

debugmode = True


class Game:
    def __init__(self, board, player1, player2=None):
        self.commode = True if player2 is None else False
        self.board = board
        self.player1 = player1
        self.player2 = player2
        self.starting_n = 9
        self.com = None
        self.on_move = 1  # 0-com 1-player1 2-player2
        self.newmuhle = False
        if player2 is None:
            self.players = [player1]
        else:
            self.players = [player1, player2]
            self.player1.set_opps(self.player2)
        self.init_Game()

    def init_Player(self, p, color):
        for i in range(self.starting_n):
            stone = Stone(color)
            p.inactiv_stones.append(stone)

    def init_Game(self):
        colors = ["dunkel", "hell"]
        i = 0
        for p in self.players:
            self.init_Player(p, colors[i])
            i += 1

    def clicked_vert(self, vn, vn_old):
        if self.commode:
            p = self.players[1 - self.on_move]
        else:
            p = self.players[self.on_move - 1]
        self.perform(p, vn, vn_old)


    def perform(self, player, vn, vn_old):
        """
        :param player:
        :param vn:
        :param vn_old:
        :return:
        """
        """
        control message
        """
        if (vn is None or (player.phase in [1, 3] and vn_old is None)) and debugmode:
            if player.phase in [1, 3]:
                print("Wrong Input: first click " + str(vn_old) + " second click " + str(vn))
            else:
                print("Wrong Input: click " + str(vn))
        else:
            if debugmode:
                print("Correct Input: first click " + str(vn_old) + " second click " + str(vn))

            if player.phase == 0:
                done = self.set_stone(player, vn)
                if done:
                    self.end_move(player)

            elif player.phase == 1:

                done = self.move_stone(player,vn,vn_old)
                if done:
                    self.end_move(player)

            elif player.phase == 2:
                done = self.rm_stone()
                if done:
                    self.end_move(player)

            elif player.phase == 3:
                done = self.jmp_stone(player,vn,vn_old)
                if done:
                    self.end_move(player)

    def get_stone_at_vert(self, q, vn):
        for st in q.activ_stones:
            if st.vert == vn:
                return st
        return None

    def set_stone(self, p, vn):
        if not self.board.vertices[vn].occ:
            stone = p.inactiv_stones.pop()
            stone.vert = vn
            stone.activ = True
            p.activ_stones.append(stone)
            self.board.vertices[vn].occ = True
            return True
        else:
            return False

    def move_stone(self, p, vn, vn_old):
        if self.board.adjazenz_matrix[vn_old, vn] == 1 and not self.board.vertices[vn].occ:
            stone = self.get_stone_at_vert(p, vn_old)
            if stone is None:
                print("Error occured while moving from "+str(vn_old)+" to "+str(vn)+ " its probably not ur Stone")
                return False
            stone.vert = vn
            self.board.vertices[vn_old].occ = False
            self.board.vertices[vn].occ = True
            if self.muhle_check(p,stone):
                self.newmuhle = True
            return True
        else:
            return False

    def rm_stone(self, p, vn):
        stone = self.get_stone_at_vert(p.opp, vn)
        if stone is None or (stone.muhle is True and stone.all_muhles is False) :
            return False
        else:
            stone.activ = False
            stone.vert = None
            ind = p.opp.activ_stones.index(stone)
            p.opp.activ_stones.pop(ind)
            self.board.vertices[vn].occ = False
            return True

    def jmp_stone(self,p,vn,vn_old):
        if not self.board.vertices[vn].occ:
            stone = self.get_stone_at_vert(p, vn_old)
            stone.vert = vn
            self.board.vertices[vn_old].occ = False
            self.board.vertices[vn].occ = True
            if self.muhle_check(p,stone):
                self.newmuhle = True
            return True
        else:
            return False


    def muhle_check(self,player,stone):  # TODO : MUHLE CHECK
        vn = stone.vert
        pass


    def set_muhles(self):
        for p in self.players:
            i = 0
            for s in p.activ_stones:
                if self.muhle_check(p,s):
                    s.muhle = True
                    i += 1
                else:
                    s.muhle = False
                if i >= len(p.aktiv_stones):
                    for s in p.aktiv_stones:
                        s.all_muhles = True
                else:
                    for s in p.aktiv_stones:
                        s.all_muhles = False

    def check_phases(self):
        for p in self.players:
            if len(p.inactiv_stones) > 0:
                p.phase = 0
            elif len(p.activ_stones) > 3:
                if not self.newmuhle:
                    p.phase = 1
                else:
                    p.phase = 2
            else:
                if not self.newmuhle:
                    p.phase = 1
                else:
                    p.phase = 3

    def end_move(self, player):
        self.check_phases()
        self.newmuhle = False
        self.set_muhles()
        if player.phase != 2:
            player.status = 2
            player.opp.status = 0
        else:
            player.status = 1

        if debugmode:
            print("Zug beendet")

        if self.commode:
            time.sleep(1)
            self.perform_com_move()
        else:
            self.on_move = self.players.index(player.opp) + 1

    def perform_com_move(self):  #todo COM
        pass
