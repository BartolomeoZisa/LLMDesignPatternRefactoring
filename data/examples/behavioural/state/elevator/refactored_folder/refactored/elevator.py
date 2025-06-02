class ElevatorError(Exception):
    pass

class ElevatorState:
    def call(self, elevator, floor):
        raise NotImplementedError

    def move(self, elevator, target_floor):
        raise NotImplementedError

    def open_doors(self, elevator):
        raise NotImplementedError

    def close_doors(self, elevator):
        raise NotImplementedError

class IdleState(ElevatorState):
    def call(self, elevator, floor):
        if floor < 0 or floor >= elevator.floors:
            raise ElevatorError("Invalid floor.")
        if elevator.current_floor == floor:
            elevator.state = DoorsOpeningState()
            return "Already on floor. " + elevator.state.open_doors(elevator)
        else:
            elevator.target_floor = floor
            elevator.state = MovingState()
            return "Elevator called to floor " + str(floor)

    def move(self, elevator, target_floor):
        raise ElevatorError("Elevator is idle, not moving.")

    def open_doors(self, elevator):
        raise ElevatorError("Elevator is idle, doors are closed.")

    def close_doors(self, elevator):
        raise ElevatorError("Elevator is idle, doors are closed.")

class MovingState(ElevatorState):
    def call(self, elevator, floor):
        raise ElevatorError("Elevator is moving, please wait.")

    def move(self, elevator, target_floor):
        while elevator.current_floor != target_floor:
            if elevator.current_floor < target_floor:
                elevator.current_floor += 1
            else:
                elevator.current_floor -= 1
        elevator.state = DoorsOpeningState()
        return "Arrived at floor " + str(elevator.current_floor) + ". "

    def open_doors(self, elevator):
        raise ElevatorError("Cannot open doors while moving.")

    def close_doors(self, elevator):
        raise ElevatorError("Doors are already closed while moving.")

class DoorsOpeningState(ElevatorState):
    def call(self, elevator, floor):
        raise ElevatorError("Doors are opening, please wait.")

    def move(self, elevator, target_floor):
        raise ElevatorError("Cannot move while doors are opening.")

    def open_doors(self, elevator):
        elevator.state = DoorsOpenState()
        return "Doors opening at floor " + str(elevator.current_floor) + ". "

    def close_doors(self, elevator):
        raise ElevatorError("Doors are opening, cannot close now.")

class DoorsOpenState(ElevatorState):
    def call(self, elevator, floor):
        raise ElevatorError("Doors are open, please wait.")

    def move(self, elevator, target_floor):
        raise ElevatorError("Cannot move, doors are open.")

    def open_doors(self, elevator):
        raise ElevatorError("Doors are already open.")

    def close_doors(self, elevator):
        elevator.state = DoorsClosingState()
        return "Closing doors. "


class DoorsClosingState(ElevatorState):
    def call(self, elevator, floor):
        raise ElevatorError("Doors are closing, please wait.")

    def move(self, elevator, target_floor):
        raise ElevatorError("Cannot move, doors are closing.")

    def open_doors(self, elevator):
        elevator.state = DoorsOpeningState()
        return "Re-opening doors. " 

    def close_doors(self, elevator):
        elevator.state = IdleState()
        return "Doors closed. Elevator is idle."

class Elevator:
    def __init__(self, floors):
        self.floors = floors
        self.current_floor = 0
        self.state = IdleState()

    def call(self, floor):
        return self.state.call(self, floor)

    def move(self, target_floor):  
        return self.state.move(self, target_floor)

    def open_doors(self):
        return self.state.open_doors(self)

    def close_doors(self):
        return self.state.close_doors(self)




