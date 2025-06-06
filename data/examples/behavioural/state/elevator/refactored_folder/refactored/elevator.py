from abc import ABC, abstractmethod

# ---------- Custom Exception ----------
class InvalidStateTransitionError(Exception):
    def __init__(self, method, state):
        super().__init__(f"Invalid operation: {method}() not allowed in {state}.")

# ---------- Base State ----------
class ElevatorState(ABC):
    def __init__(self, elevator):
        self.elevator = elevator

    def call_to_up(self):
        raise InvalidStateTransitionError("call_to_up", self.__class__.__name__)

    def call_to_down(self):
        raise InvalidStateTransitionError("call_to_down", self.__class__.__name__)

    def notify_arrived(self):
        raise InvalidStateTransitionError("notify_arrived", self.__class__.__name__)

    def notify_doors_opened(self):
        raise InvalidStateTransitionError("notify_doors_opened", self.__class__.__name__)

    def notify_door_closed_up(self):
        raise InvalidStateTransitionError("notify_door_closed_up", self.__class__.__name__)

    def notify_door_closed_down(self):
        raise InvalidStateTransitionError("notify_door_closed_down", self.__class__.__name__)

# ---------- Elevator Context ----------
class Elevator:
    def __init__(self):
        self.state = IdleDownState(self)

    def set_state(self, new_state):
        print(f"Transitioning to: {new_state.__class__.__name__}")
        self.state = new_state

    def call_to_up(self):
        self.state.call_to_up()

    def call_to_down(self):
        self.state.call_to_down()

    def sensor_arrival_triggered(self):
        self.state.notify_arrived()

    def sensor_doors_opened(self):
        self.state.notify_doors_opened()

    def sensor_door_closed_up(self):
        self.state.notify_door_closed_up()

    def sensor_door_closed_down(self):
        self.state.notify_door_closed_down()

# ---------- Concrete States ----------
class IdleDownState(ElevatorState):
    def call_to_up(self):
        print("Going up from bottom floor...")
        self.elevator.set_state(MovingUpwardsState(self.elevator))

class IdleUpState(ElevatorState):
    def call_to_down(self):
        print("Going down from top floor...")
        self.elevator.set_state(MovingDownwardsState(self.elevator))

class MovingUpwardsState(ElevatorState):
    def notify_arrived(self):
        print("Arrived at top floor.")
        self.elevator.set_state(DoorsOpeningState(self.elevator))

class MovingDownwardsState(ElevatorState):
    def notify_arrived(self):
        print("Arrived at bottom floor.")
        self.elevator.set_state(DoorsOpeningState(self.elevator))

class DoorsOpeningState(ElevatorState):
    def notify_doors_opened(self):
        print("Doors are fully opened.")
        self.elevator.set_state(DoorsClosingState(self.elevator))

class DoorsClosingState(ElevatorState):
    def notify_door_closed_up(self):
        print("Doors closed at top floor.")
        self.elevator.set_state(IdleUpState(self.elevator))

    def notify_door_closed_down(self):
        print("Doors closed at bottom floor.")
        self.elevator.set_state(IdleDownState(self.elevator))





