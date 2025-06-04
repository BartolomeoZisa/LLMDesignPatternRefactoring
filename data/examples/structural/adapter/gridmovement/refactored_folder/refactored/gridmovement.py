class GridMover:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def move(self, direction):
        if direction == "up":
            self.y -= 1
        elif direction == "down":
            self.y += 1
        elif direction == "left":
            self.x -= 1
        elif direction == "right":
            self.x += 1
        else:
            # Instead of print, raise an error:
            raise ValueError(f"[GridMover] Unknown direction: {direction}")

    def get_position(self):
        return self.x, self.y


class KeyboardController:
    def __init__(self, mover: GridMover):
        self.mover = mover

    def execute_commands(self, commands):
        for command in commands:
            print(f"[KeyboardController] Moving {command}")
            self.mover.move(command)
            print(f"Current Position: {self.mover.get_position()}")


class TouchAdapter:
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







