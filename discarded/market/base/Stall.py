from abc import ABC, abstractmethod


class Stall:
    def __init__(self):
        self.state = FreeState(self)
    
    def set_state(self, state):
        self.state = state
    
    def assign(self):
        
        if isinstance(self.state, FreeState):
            print("Stall assigned.")
            self.set_state(AssignedState(self))
        elif isinstance(self.state, AssignedState):
            print("Already assigned.")
        elif isinstance(self.state, OccupiedState):
            print("Cannot assign while occupied.")
        elif isinstance(self.state, MaintenanceState):
            print("Cannot assign. Stall is under maintenance.")
    
    def start_market(self):
        if isinstance(self.state, FreeState):
            print("Cannot start market without assignment.")
        elif isinstance(self.state, AssignedState):
            print("Market started.")
            self.set_state(OccupiedState(self))
        elif isinstance(self.state, OccupiedState):
            print("Already in market.")
        elif isinstance(self.state, MaintenanceState):
            print("Cannot start market. Stall is under maintenance.")
    
    def end_market(self):
        if isinstance(self.state, FreeState):
            print("Market is not running.")
        elif isinstance(self.state, AssignedState):
            print("Market not started yet.")
        elif isinstance(self.state, OccupiedState):
            print("Market ended. Moving to free state.")
            self.set_state(FreeState(self))
        elif isinstance(self.state, MaintenanceState):
            print("Market is not running.")
    
    def report_issue(self):
        if isinstance(self.state, FreeState):
            print("Issue reported. Moving to maintenance.")
            self.set_state(MaintenanceState(self))
        elif isinstance(self.state, AssignedState):
            print("Issue reported. Moving to maintenance.")
            self.set_state(MaintenanceState(self))
        elif isinstance(self.state, OccupiedState):
            print("Issue reported. Moving to maintenance.")
            self.set_state(MaintenanceState(self))
        elif isinstance(self.state, MaintenanceState):
            print("Already under maintenance.")
    
    def finish_maintenance(self):
        if isinstance(self.state, FreeState):
            print("Already in a free state.")
        elif isinstance(self.state, AssignedState):
            print("Cannot finish maintenance in assigned state.")
        elif isinstance(self.state, OccupiedState):
            print("Cannot finish maintenance in occupied state.")
        elif isinstance(self.state, MaintenanceState):
            print("Maintenance finished. Moving to free state.")
            self.set_state(FreeState(self))


# State Classes
class StallState(ABC):
    def __init__(self, stall):
        self.stall = stall


class FreeState(StallState):
    def __init__(self, stall):
        super().__init__(stall)
    


class AssignedState(StallState):
    def __init__(self, stall):
        super().__init__(stall)


class OccupiedState(StallState):
    def __init__(self, stall):
        super().__init__(stall)



class MaintenanceState(StallState):
    def __init__(self, stall):
        super().__init__(stall)

