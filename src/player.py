class Player:
    def __init__(self):
        self.phase = 0  # 0-setzen 1-ziehen 2-entfernen 3-springen
        self.inactiv_stones = []
        self.activ_stones = []
        self.status = 0  # 0-warte auf Zug, 1-warte weiter 2-zug beendet
        self.opp = None
        self.com = False


    def set_opps(self, player2):
        self.opp = player2
        player2.opp = self