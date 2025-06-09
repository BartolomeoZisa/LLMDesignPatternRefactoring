import math

class RoundHole:
    def __init__(self, radius):
        if radius <= 0:
            raise ValueError("Hole radius must be positive.")
        self._radius = radius

    def get_radius(self):
        return self._radius

    def fits(self, peg):
        return self.get_radius() >= peg.get_radius()
    
    def fits_other(self, peg, type):
        if type == "square":
            return self.get_radius() >= peg.get_radius() * math.sqrt(2) / 2
        else:
            raise ValueError("Unsupported peg type.")
    


class RoundPeg:
    def __init__(self, radius):
        if radius <= 0:
            raise ValueError("Peg radius must be positive.")
        self._radius = radius

    def get_radius(self):
        return self._radius


class SquarePeg:
    def __init__(self, width):
        if width <= 0:
            raise ValueError("Square peg width must be positive.")
        self._width = width

    def get_width(self):
        return self._width
