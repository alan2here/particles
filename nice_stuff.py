import math # sqrt

class vec2: pass

class vec2:
    def __init__(self, x : float, y : float):
        self.x = x
        self.y = y

    def __eq__(self, other : vec2) -> bool:
        return self.x == other.x and self.y == other.y

    def __add__(self, other : vec2) -> vec2:
        return vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other : vec2) -> vec2:
        return vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, scale : float) -> vec2:
        return vec2(self.x * scale, self.y * scale)

    def __truediv__(self, scale : float) -> vec2:
        if (scale == 0):
            raise ZeroDivisionError("vec2.__truediv__ --> cannot divide by 0")
        return vec2(self.x / scale, self.y / scale)

    def dist(self, other : vec2) -> float:
        dif = self - other
        return math.sqrt(dif.x ** 2 + dif.y ** 2)

    def length(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def normalise(self) -> vec2:
        if self.x == 0 and self.y == 0:
            raise ZeroDivisionError("vec2.normalise() --> cannot normalize vec2(0, 0)")
        return self / self.length()
