class Stone:
    def __init__(self):
        self.vert = None
        self.color = ""
        self.muhle = False

    def removable(self):
        return not self.muhle
