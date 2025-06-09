from abc import ABC, abstractmethod

# ---------- Custom Exception ----------
class InvalidStateTransitionError(Exception):
    def __init__(self, method, state):
        super().__init__(f"Invalid operation: {method}() not allowed in {state}.")

# ---------- Base State ----------
class ElevatorState(ABC):
    def __init__(self, elevator):
        self.elevator = elevator

    def call(self, direction):
        raise InvalidStateTransitionError("call", self.__class__.__name__)

    def notify_arrived(self):
        raise InvalidStateTransitionError("notify_arrived", self.__class__.__name__)

    def notify_doors_opened(self):
        raise InvalidStateTransitionError("notify_doors_opened", self.__class__.__name__)

    def notify_door_closed(self):
        raise InvalidStateTransitionError("notify_door_closed", self.__class__.__name__)

# ---------- Elevator Context ----------
class Elevator:
    def __init__(self):
        self.state = IdleDownState(self)

    def set_state(self, new_state):
        print(f"Transitioning to: {new_state.__class__.__name__}")
        self.state = new_state

    def call(self, direction):
        self.state.call(direction)

    def sensor_arrival_triggered(self):
        self.state.notify_arrived()

    def sensor_doors_opened(self):
        self.state.notify_doors_opened()

    def sensor_door_closed(self):
        self.state.notify_door_closed()

# ---------- Concrete States ----------
class IdleDownState(ElevatorState):
    def call(self, direction):
        if direction == "up":
            print("Going up from bottom floor...")
            self.elevator.set_state(MovingUpwardsState(self.elevator))
        else:
            self.elevator.set_state(DoorsOpeningDownState(self.elevator))

class IdleUpState(ElevatorState):
    def call(self, direction):
        if direction == "down":
            print("Going down from top floor...")
            self.elevator.set_state(MovingDownwardsState(self.elevator))
        else:
            self.elevator.set_state(DoorsOpeningUpState(self.elevator))

class MovingUpwardsState(ElevatorState):
    def notify_arrived(self):
        print("Arrived at top floor.")
        self.elevator.set_state(DoorsOpeningUpState(self.elevator))

class MovingDownwardsState(ElevatorState):
    def notify_arrived(self):
        print("Arrived at bottom floor.")
        self.elevator.set_state(DoorsOpeningDownState(self.elevator))

class DoorsOpeningUpState(ElevatorState):
    def notify_doors_opened(self):
        print("Doors opened at top floor.")
        self.elevator.set_state(DoorsClosingUpState(self.elevator))

class DoorsOpeningDownState(ElevatorState):
    def notify_doors_opened(self):
        print("Doors opened at bottom floor.")
        self.elevator.set_state(DoorsClosingDownState(self.elevator))

class DoorsClosingUpState(ElevatorState):
    def notify_door_closed(self):
        print("Doors closed at top floor.")
        self.elevator.set_state(IdleUpState(self.elevator))

class DoorsClosingDownState(ElevatorState):
    def notify_door_closed(self):
        print("Doors closed at bottom floor.")
        self.elevator.set_state(IdleDownState(self.elevator))






