import numpy as np
import math as m


class System():
    def __init__(self, epsilon, gamma):
        self.sources = []
        self.walls = []
        self.epsilon = epsilon
        self.gamma = gamma

    def add_source(self, point):
        self.sources.append(point)

    def remove_source(self, point):
        self.sources.remove(point)

    def clear_sources(self):
        self.sources.clear()

    def add_wall(self, wall):
        self.walls.append(wall)


    def field(self, X, Y):
        u, v = X.shape
        size = np.size(X)
        X.shape = (size)
        Y.shape = (size)
        Vx = np.zeros((u, v))
        Vy = np.zeros((u, v))

        for sources in self.sources:
            tX = [X[i] - sources.x for i in range(np.size(X))]
            tY = [Y[i] - sources.y for i in range(np.size(Y))]
            vectors = [sources.vector_at_point(tX[i], tY[i], self.epsilon, self.gamma) for i in range(size)]
            xv, yv = zip(*vectors)
            xv = np.array(xv, dtype=np.float)
            yv = np.array(yv, dtype=np.float)
            xv.shape = (u,v)
            yv.shape = (u,v)
            Vx = Vx + xv
            Vy = Vy + yv

        return Vx, Vy
