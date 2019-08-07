class Player:
    def __init__(self):
        self.phase = 0  # 0-setzen 1-ziehen 2-entfernen 3-springen
        self.n_ia = 4
        self.n_a = 0
        self.inaktiv_stones = []
        self.aktiv_stones = []
        self.t_lm = 0
        self.status = 0  # 0-warte auf Zug, 1-warte weiter 2-zug beendet
        self.opp = None
        self.com = False

    def set_opps(self, player2):
        self.opp = player2
        player2.opp = self

    def action(self, board, target, stone=None):  #
        self.status = 0
        print(self.phase)
        print(target)
        print(stone)
        if self.phase == 0:  # setzen
            print(self.inaktiv_stones)
            print(self.aktiv_stones)
            stone = self.inaktiv_stones.pop()
            self.aktiv_stones.append(stone)
            if board.path_check(self, stone, target):  #
                stone.aktiv = True
                stone.vert = target
                board.vertices[stone.vert].occ = True
                self.n_ia -= 1
                self.n_a += 1
                self.status = 2  # end of move
            else:
                self.decline()
            if self.n_ia == 0:
                self.change_phases(1)

        elif self.phase == 1:  # ziehen
            if target is not None and stone is not None:
                if board.path_check(self, stone, target):
                    oldvert = stone.vert
                    stone.vert = target
                    board.vertices[oldvert].occ = False
                    board.vertices[stone.vert].occ = True
                    m, n = self.check_muhle(board, stone)
                    if m:  # got a muhle               todo: double muhle
                        self.change_phases(2)
                        self.status = 1  # move done but another follows
                    else:
                        self.status = 2  # end of move
                else:
                    self.decline()

        elif self.phase == 2:  # entfernen
            if any(stone for stone in self.opp.stones if stone.vert == target and not stone.muhle):
                stonex = [stone for stone in self.opp.stones if stone.vert == target][0]
                if board.path_check(self, stonex, target):
                    board.vertices[stonex.vert].occ = False
                    stonex.vert = None
                    self.opp.aktiv_stones.pop(self.opp.aktiv_stones.index(stonex))
                    self.status = 2  # end of move
                    if self.opp.n_a <= 3:
                        self.opp.change_phases(3)  # springen
                    if self.n_a <= 3:
                        self.change_phases(3)  # springen
                    elif self.n_ia > 0:
                        self.change_phases(0)  # setzen
                    else:
                        self.change_phases(1)  # ziehen

        elif self.phase == 3:  # springen
            if board.path_check(self, stone, target):
                board.vertices[stone.vert].occ = False
                board.vertices[target].occ = True
                m, n = self.check_muhle(board, stone)
                if m:                                   # got a muhle
                    self.change_phases(2)
                    self.status = 1  # move done but another follows
                else:
                    self.status = 2  # end of move

    def check_muhle(self, board, stone):
        vert = board.vertices[stone.vert]
        x = vert.pos_x
        y = vert.poy_y
        nby = [stone for stone in self.stones if board.vertices[stone.vert].pos_x == x]
        nbx = [stone for stone in self.stones if board.vertices[stone.vert].pos_y == y]
        if len(nbx) == len(nby) == 2:
            nb = nby + nbx + [stone]
            return True, nb
        elif len(nby) == 2:
            nby = nby.append(stone)
            return True, nby
        elif len(nbx) == 2:
            nbx = nbx.append(stone)
            return True, nbx
        else:
            return False, None

    def change_phases(self, newphase):
        self.phase = newphase

    def check_stones(self, board):
        for stone in self.stones:
            m, nb = self.check_muhle(board, stone)
            if m:
                for st in nb:
                    st.muhle = True
            else:
                stone.muhle = False
    def end_move(self):
        pass
    def decline(self):
        print("Wrong")
