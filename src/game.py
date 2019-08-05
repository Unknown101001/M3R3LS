class Game:
    def __init__(self,board, player1, player2 = None):
        self.commode = True if player2 is None else False
        self.board = board
        self.player1 = player1
        self.player2 = player2