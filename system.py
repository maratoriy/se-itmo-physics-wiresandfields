import numpy as np
import math as m


class System():
    def __init__(self, epsilon, gamma):
        self.objects = []
        self.walls = []
        self.epsilon = epsilon
        self.gamma = gamma

    def addObject(self, point):
        self.objects.append(point)

    def removeObject(self, point):
        self.objects.remove(point)

    def removeAllObjects(self):
        self.objects.clear()

    def addWall(self, wall):
        self.walls.append(wall)

    def compute(self, i, X, Y, R, I):
        dist = m.sqrt(m.pow(Y[i], 2) + m.pow(X[i], 2))
        if(dist<R):
            H = I / (2 * m.pi * R ** 2) * dist
            return self.gamma*H
        else:
            return (self.gamma * I) / (2 * m.pi * dist)



    def computeX(self, i, X, Y, R, I):
        dist = m.sqrt(m.pow(Y[i], 2) + m.pow(X[i], 2))
        B = self.compute(i, X, Y, R, I)
        Bx = B * (X[i]/dist)

        return Bx

    def computeY(self, i, X, Y, R, I):
        dist = m.sqrt(m.pow(Y[i], 2) + m.pow(X[i], 2))
        B = self.compute(i, X, Y, R, I)
        By = B * (Y[i]/dist)

        return By


    def field(self, X, Y):
        u, v = X.shape
        size = np.size(X)
        X.shape = (size)
        Y.shape = (size)
        Vx = np.zeros((u, v))
        Vy = np.zeros((u, v))

        for object in self.objects:
            tX = [X[i] - object.x for i in range(np.size(X))]
            tY = [Y[i] - object.y for i in range(np.size(Y))]
            Bx = np.array([self.computeX(i, tX, tY, object.size, object.electric) for i in range(size)], dtype=np.float)
            By = np.array([self.computeY(i, tX, tY, object.size, object.electric) for i in range(size)], dtype=np.float)
            Bx.shape = (u, v)
            Vx = Vx + Bx
            By.shape = (u, v)
            Vy = Vy + By
        return Vx, Vy
