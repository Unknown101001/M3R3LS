class Stone:
    def __init__(self):
        self.status = 0  # 0 - inaktiv, 1 - aktiv, 2 - springer, 3 - geschlagen
        self.vert = None
        self.color = ""
        self.muhle = False
        self.targeted = False

    def removable(self):
        return (not self.muhle and self.status in [1, 2])
