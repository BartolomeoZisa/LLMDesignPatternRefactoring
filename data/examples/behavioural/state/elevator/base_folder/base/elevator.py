from abc import ABC

# ---------- Custom Exception ----------
class InvalidStateTransitionError(Exception):
    def __init__(self, method, state):
        super().__init__(f"Invalid operation: {method}() not allowed in {state}.")

# ---------- Base State ----------
class ElevatorState(ABC):
    pass

# ---------- Concrete States (empty, just markers) ----------
class IdleDownState(ElevatorState): pass
class IdleUpState(ElevatorState): pass
class MovingUpwardsState(ElevatorState): pass
class MovingDownwardsState(ElevatorState): pass
class DoorsOpeningState(ElevatorState): pass
class DoorsClosingState(ElevatorState): pass

# ---------- Elevator Context ----------
class Elevator:
    def __init__(self):
        self.state = IdleDownState()

    def set_state(self, new_state):
        print(f"Transitioning to: {new_state.__class__.__name__}")
        self.state = new_state

    def call_to_up(self):
        state = self.state.__class__.__name__
        if state == "IdleDownState":
            print("Going up from bottom floor...")
            self.set_state(MovingUpwardsState())
        else:
            raise InvalidStateTransitionError("call_to_up", state)

    def call_to_down(self):
        state = self.state.__class__.__name__
        if state == "IdleUpState":
            print("Going down from top floor...")
            self.set_state(MovingDownwardsState())
        else:
            raise InvalidStateTransitionError("call_to_down", state)

    def sensor_arrival_triggered(self):
        state = self.state.__class__.__name__
        if state == "MovingUpwardsState":
            print("Arrived at top floor.")
            self.set_state(DoorsOpeningState())
        elif state == "MovingDownwardsState":
            print("Arrived at bottom floor.")
            self.set_state(DoorsOpeningState())
        else:
            raise InvalidStateTransitionError("notify_arrived", state)

    def sensor_doors_opened(self):
        state = self.state.__class__.__name__
        if state == "DoorsOpeningState":
            print("Doors are fully opened.")
            self.set_state(DoorsClosingState())
        else:
            raise InvalidStateTransitionError("notify_doors_opened", state)

    def sensor_door_closed_up(self):
        state = self.state.__class__.__name__
        if state == "DoorsClosingState":
            print("Doors closed at top floor.")
            self.set_state(IdleUpState())
        else:
            raise InvalidStateTransitionError("notify_door_closed_up", state)

    def sensor_door_closed_down(self):
        state = self.state.__class__.__name__
        if state == "DoorsClosingState":
            print("Doors closed at bottom floor.")
            self.set_state(IdleDownState())
        else:
            raise InvalidStateTransitionError("notify_door_closed_down", state)




