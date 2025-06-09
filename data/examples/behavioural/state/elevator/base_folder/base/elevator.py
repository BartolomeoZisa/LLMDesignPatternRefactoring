# ---------- Custom Exception ----------
class InvalidStateTransitionError(Exception):
    def __init__(self, method, state):
        super().__init__(f"Invalid operation: {method}() not allowed in {state}.")

# ---------- Elevator State Classes ----------
class IdleDownState:
    def __init__(self, elevator):
        self.elevator = elevator

class IdleUpState:
    def __init__(self, elevator):
        self.elevator = elevator

class MovingUpwardsState:
    def __init__(self, elevator):
        self.elevator = elevator

class MovingDownwardsState:
    def __init__(self, elevator):
        self.elevator = elevator

class DoorsOpeningUpState:
    def __init__(self, elevator):
        self.elevator = elevator

class DoorsOpeningDownState:
    def __init__(self, elevator):
        self.elevator = elevator

class DoorsClosingUpState:
    def __init__(self, elevator):
        self.elevator = elevator

class DoorsClosingDownState:
    def __init__(self, elevator):
        self.elevator = elevator

# ---------- Elevator Context ----------
class Elevator:
    def __init__(self):
        self.state = IdleDownState(self)

    def set_state(self, new_state_instance):  # Expecting an object, not a class
        print(f"Transitioning to: {type(new_state_instance).__name__}")
        self.state = new_state_instance

    def call(self, direction):
        if isinstance(self.state, IdleDownState):
            if direction == "up":
                print("Going up from bottom floor...")
                self.set_state(MovingUpwardsState(self))
            else:
                self.set_state(DoorsOpeningDownState(self))
        elif isinstance(self.state, IdleUpState):
            if direction == "down":
                print("Going down from top floor...")
                self.set_state(MovingDownwardsState(self))
            else:
                self.set_state(DoorsOpeningUpState(self))
        else:
            raise InvalidStateTransitionError("call", type(self.state).__name__)

    def sensor_arrival_triggered(self):
        if isinstance(self.state, MovingUpwardsState):
            print("Arrived at top floor.")
            self.set_state(DoorsOpeningUpState(self))
        elif isinstance(self.state, MovingDownwardsState):
            print("Arrived at bottom floor.")
            self.set_state(DoorsOpeningDownState(self))
        else:
            raise InvalidStateTransitionError("notify_arrived", type(self.state).__name__)

    def sensor_doors_opened(self):
        if isinstance(self.state, DoorsOpeningUpState):
            print("Doors opened at top floor.")
            self.set_state(DoorsClosingUpState(self))
        elif isinstance(self.state, DoorsOpeningDownState):
            print("Doors opened at bottom floor.")
            self.set_state(DoorsClosingDownState(self))
        else:
            raise InvalidStateTransitionError("notify_doors_opened", type(self.state).__name__)

    def sensor_door_closed(self):
        if isinstance(self.state, DoorsClosingUpState):
            print("Doors closed at top floor.")
            self.set_state(IdleUpState(self))
        elif isinstance(self.state, DoorsClosingDownState):
            print("Doors closed at bottom floor.")
            self.set_state(IdleDownState(self))
        else:
            raise InvalidStateTransitionError("notify_door_closed", type(self.state).__name__)
