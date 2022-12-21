from abc import abstractmethod
import math as m
import numpy as np


class MagneticSource:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def dist(self, x, y):
        return np.hypot(self.x-x, self.y-y)

    @abstractmethod
    def vector_at_point(self, dx, dy, epsilon, gamma):
        pass

    @abstractmethod
    def hit(self, x, y):
        pass

    @abstractmethod
    def intersect(self, x, y):
        pass


class Wire(MagneticSource):
    def __init__(self, x, y, radius, electric):
        super().__init__(x, y)
        self.radius = radius
        self.electric = electric

    def vector_at_point(self, dx, dy, epsilon, gamma):
        dist = np.hypot(dx, dy)
        if dist < self.radius:
            H = self.electric / (2 * m.pi * self.radius ** 2) * dist
            B = gamma * H
        else:
            B = (gamma * self.electric) / (2 * m.pi * dist)
        return -B * (dy / dist), B * (dx / dist)

    def hit(self, x, y):
        return (x - self.x) ** 2 + (y - self.y) ** 2 <= self.radius ** 2


