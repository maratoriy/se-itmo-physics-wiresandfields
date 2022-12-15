class Wire():
    def __init__(self, x, y, size, electric):
        self.x = x
        self.y = y
        self.size = size
        self.electric = electric

    def hit(self, x, y):
        return (x - self.x) ** 2 + (y - self.y) ** 2 <= self.size ** 2
