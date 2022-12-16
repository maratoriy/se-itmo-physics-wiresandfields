from abc import abstractmethod
import math as m
import numpy as np


class MagneticSource:
    @staticmethod
    def dist(x, y):
        return np.hypot(x, y)

    @abstractmethod
    def vector_at_point(self, dx, dy, epsilon, gamma):
        pass


class Wire(MagneticSource):
    def __init__(self, x, y, radius, electric):
        self.x = x
        self.y = y
        self.radius = radius
        self.electric = electric

    def vector_at_point(self, dx, dy, epsilon, gamma):
        dist = self.dist(dx, dy)
        if dist < self.radius:
            H = self.electric / (2 * m.pi * self.radius ** 2) * dist
            B = gamma * H
        else:
            B = (gamma * self.electric) / (2 * m.pi * dist)
        return -B * (dy / dist), B * (dx / dist)

    def hit(self, x, y):
        return (x - self.x) ** 2 + (y - self.y) ** 2 <= self.radius ** 2
