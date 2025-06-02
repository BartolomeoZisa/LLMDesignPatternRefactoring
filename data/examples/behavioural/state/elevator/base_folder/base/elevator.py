class ElevatorError(Exception):
    """Custom exception for elevator errors"""
    pass


class Elevator:
    def __init__(self, floors):
        self.floors = floors
        self.current_floor = 0
        self.target_floor = None
        self.state = "idle"  # idle, moving, doors_opening, doors_open, doors_closing
    
    def _validate_floor(self, floor):
        """Validate if the floor number is valid"""
        if floor < 1 or floor > self.floors:
            raise ElevatorError("Invalid floor.")
    
    def call(self, floor):
        """Call elevator to a specific floor"""
        self._validate_floor(floor)
        
        # Check current state restrictions
        if self.state == "moving":
            raise ElevatorError("Elevator is moving, please wait.")
        elif self.state in ["doors_opening", "doors_open"]:
            raise ElevatorError("Doors are open, please wait.")
        
        # If already on the requested floor
        if self.current_floor == floor:
            self.state = "doors_opening"
            return "Already on floor. Doors opening."
        
        # Set target and change state to moving
        self.target_floor = floor
        self.state = "moving"
        return f"Elevator called to floor {floor}"
    
    def move(self, floor):
        """Move elevator to target floor"""
        if self.state == "idle":
            raise ElevatorError("Elevator is idle, not moving.")
        elif self.state in ["doors_opening", "doors_open"]:
            raise ElevatorError("Cannot move, doors are open.")
        elif self.state == "doors_closing":
            raise ElevatorError("Cannot move, doors are closing.")
        elif self.state != "moving":
            raise ElevatorError("Cannot move in current state.")
        
        # Move to the floor
        self.current_floor = floor
        self.target_floor = None
        self.state = "doors_opening"  # After moving, doors start opening
        return f"Arrived at floor {floor}"
    
    def open_doors(self):
        """Open elevator doors"""
        if self.state == "idle":
            raise ElevatorError("Elevator is idle, doors are closed.")
        elif self.state == "moving":
            raise ElevatorError("Cannot open doors while moving.")
        elif self.state == "doors_open":
            raise ElevatorError("Doors are already open.")
        elif self.state == "doors_opening":
            # Transition from opening to open
            self.state = "doors_open"
            return f"Doors opening at floor {self.current_floor}"
        elif self.state == "doors_closing":
            # Re-opening while closing
            self.state = "doors_opening"
            return "Re-opening doors."
        
        # Default case - open doors
        self.state = "doors_opening"
        return f"Doors opening at floor {self.current_floor}"
    
    def close_doors(self):
        """Close elevator doors"""
        if self.state == "idle":
            raise ElevatorError("Elevator is idle, doors are closed.")
        elif self.state == "doors_opening":
            raise ElevatorError("Doors are opening, cannot close now.")
        elif self.state == "doors_open":
            self.state = "doors_closing"
            return "Closing doors."
        elif self.state == "doors_closing":
            # Complete the closing and return to idle
            self.state = "idle"
            return "Doors closed."
        
        raise ElevatorError("Cannot close doors in current state.")



