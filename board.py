import numpy as np


class Board:
    def __init__(self, vertices):
        """
        :param vertices: list of coordinates
        """
        self.vertices = vertices
        self.n = n = len(vertices)
        self.adjazenz_matrix = np.zeros((n, n))
        self.background = ""
        self.color = "#000000"
        self.width = 0
        self.height = 0

    def path_check(self, player, stone, vertex):
        """
        :param player:
        :param stone:
        :param vertex:
        :return:
        """
        current_v = stone.vert
        if player.phase == 0:  # setzen
            if not vertex.occ:
                return True
        elif player.phase == 1:  # ziehen
            if self.adjazenz_matrix[current_v, vertex] == 1 and not vertex.occ:
                return True
        elif player.phase == 2:  # entfernen
            if stone.removable():
                return True
        elif player.phase == 3:  # springen
            if not vertex.occ:
                return True

        return False


