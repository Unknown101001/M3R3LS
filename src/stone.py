class Stone:
    def __init__(self,color):
        self.vert = None
        self.color = color
        self.muhle = False
        self.aktiv =  False

    def removable(self):
        return not self.muhle
