import numpy as np
from vertex import *

coords = [(0, 0),
          (3, 0),
          (6, 0),
          (1, 1),
          (3, 1),
          (5, 1),
          (2, 2),
          (3, 2),
          (4, 2),
          (0, 3),
          (1, 3),
          (2, 3),
          (4, 3),
          (5, 3),
          (6, 3),
          (2, 4),
          (3, 4),
          (4, 4),
          (1, 5),
          (3, 5),
          (5, 5),
          (0, 6),
          (3, 6),
          (6, 6),
          ]
edges = [(1, 2),
         (2, 3),
         (2, 5),
         (1, 10),
         (3, 15),
         (10, 11),
         (11, 12),
         (11, 4),
         (4, 5),
         (5, 8),
         (5, 6),
         (6, 14),
         (13, 14),
         (15, 14),
         (13, 9),
         (9, 8),
         (7, 8),
         (7, 12),
         (16, 12),
         (17, 16),
         (17, 18),
         (13, 18),
         (10, 22),
         (23, 22),
         (23, 24),
         (15, 24),
         (14, 21),
         (20, 21),
         (20, 19),
         (11, 19),
         (17, 20)
         ]


class Board:
    def __init__(self, vertices = None):
        """
        :param vertices: list of coordinates
        """
        if vertices is None:
            self.vertices = []
            for tup in coords:
                v = [Vertex(tup[0], tup[1])]
                self.vertices += v
            self.n = n = 24
            self.adjazenz_matrix = np.zeros((n, n))
            for e in edges:
                self.adjazenz_matrix[e[0]-1, e[1]-1] = self.adjazenz_matrix[e[1]-1, e[0]-1] = 1
            self.background = "#D8D8D8"
            self.color = "#000000"
        else:
            self.vertices = vertices
            self.n = n = len(vertices)
            self.adjazenz_matrix = np.zeros((n, n))
            self.background = ""
            self.color = "#000000"

    def path_check(self, player, stone, vertex):
        """
        :param player:
        :param stone:
        :param vertex:
        :return:
        """
        vertexocc = self.vertices[vertex].occ
        current_v = stone.vert
        if player.phase == 0:  # setzen
            if not vertexocc:
                return True
        elif player.phase == 1:  # ziehen
            if self.adjazenz_matrix[current_v, vertex] == 1 and not vertexocc:
                return True
        elif player.phase == 2:  # entfernen
            if stone.removable():
                return True
        elif player.phase == 3:  # springen
            if not vertexocc:
                return True
        return False
