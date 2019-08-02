class Player:
    def __init__(self):
        self.phase = 0  # 0-setzen 1-ziehen 2-entfernen 3-springen
        self.n_ia = 9
        self.n_a = 0
        self.stones = []
        self.t_lm = 0
        self.status = 0 #0-warte auf Zug, 1-Zug beendet

    def action(self,board,target,stone=None):#
        if self.phase == 0:  # setzen
            stone = next([stone for stone in self.stones if stone.status==0 ])
            if board.path_check(self,stone,target):#
                stone.vert = target
                self.n_ia -= 1
                self.n_a += 1
                self.status = 1
            else: self.decline()
        elif self.phase == 1:  # ziehen
            if board.path_check(self,stone,target):
                stone.vert = target
                m,n = self.check_muhle(board,stone)
                if m:
                    self.change_phases(self,2)
                    self.status = 1


        elif self.phase == 2:  # entfernen

        elif self.phase == 3:  # springen

    def check_muhle(self, board , stone):
        vert = board.vertices[stone.vert]
        x = vert.pos_x
        y = vert.poy_y
        nby = [stone for stone in self.stones if board.vertices[stone.vert].pos_x == x]
        nbx = [stone for stone in self.stones if board.vertices[stone.vert].pos_y == y]
        if len(nbx)==len(nby)==2:
            nb = nby + nbx + [stone]
            return True,nb
        elif len(nby)==2:
            nby = nby.append(stone)
            return True,nby
        elif len(nbx)==2:
            nbx = nbx.append(stone)
            return True,nbx
        else:
            return False,None
    def change_phases(self,newphase):
        self.phase = newphase
    def check_stones(self,board):
        for stone in self.stones:
            m,nb = self.check_muhle(board,stone)
            if m:
                for st in nb:
                    st.muhle = True
            else: stone.muhle = False

    def decline(self):
        pass
