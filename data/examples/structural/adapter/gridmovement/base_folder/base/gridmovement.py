class GridMover:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.bounds = ((-3, -3), (3, 3)) 

    def check_bounds(self):
        if not (self.bounds[0][0] <= self.x <= self.bounds[1][0] and
                self.bounds[0][1] <= self.y <= self.bounds[1][1]):
            raise ValueError(f"[GridMover] Position out of bounds: ({self.x}, {self.y})")
        

    def move(self, direction):
        if direction == "up":
            self.y -= 1
            self.check_bounds()
        elif direction == "down":
            self.y += 1
            self.check_bounds()
        elif direction == "left":
            self.x -= 1
            self.check_bounds()
        elif direction == "right":
            self.x += 1
            self.check_bounds()
        else:
            raise ValueError(f"[GridMover] Unknown direction: {direction}")

    def get_position(self):
        return self.x, self.y




