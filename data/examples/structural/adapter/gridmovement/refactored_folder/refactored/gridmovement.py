from abc import ABC, abstractmethod

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

    def get_position(self):
        return self.x, self.y


class ITouchController(ABC):
    @abstractmethod
    def swipe(self, gesture):
        pass



class TouchAdapter(ITouchController):
    def __init__(self, mover: GridMover):
        self.mover = mover
        self.gesture_to_direction = {
            "swipe_up": "up",
            "swipe_down": "down",
            "swipe_left": "left",
            "swipe_right": "right"
        }

    def swipe(self, gesture):
        direction = self.gesture_to_direction.get(gesture)
        if direction:
            print(f"[TouchAdapter] Swiping {gesture} -> {direction}")
            self.mover.move(direction)
            print(f"Current Position: {self.mover.get_position()}")
        else:
            # Raise error here as well
            raise ValueError(f"[TouchAdapter] Unknown gesture: {gesture}")







