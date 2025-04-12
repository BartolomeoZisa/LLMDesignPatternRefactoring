from abc import ABC, abstractmethod


class Stall:
    def __init__(self):
        self.state = FreeState(self)
    
    def set_state(self, state):
        self.state = state
    
    def assign(self): 
        if isinstance(self.state, FreeState):
            print("Stall assigned.")
            self.set_state(OccupiedState(self))
        elif isinstance(self.state, OccupiedState):
            raise Exception("Cannot assign while occupied.")
        elif isinstance(self.state, OccupiedMaintenanceState):
            raise Exception("Cannot assign. Stall is under maintenance.")
        elif isinstance(self.state, FreeMaintenanceState):
            raise Exception("Cannot assign. Stall is under maintenance.")
    
    def end_market(self):
        if isinstance(self.state, FreeState):
            raise Exception("Market is not running.")
        elif isinstance(self.state, OccupiedState):
            print("Market ended. Moving to free state.")
            self.set_state(FreeState(self))
        elif isinstance(self.state, FreeMaintenanceState):
            raise Exception("Market is not running.")
        elif isinstance(self.state, OccupiedMaintenanceState):
            print("Market ended, changing maintenance.")
            self.set_state(FreeMaintenanceState(self))
    
    def report_issue(self):
        if isinstance(self.state, FreeState):
            print("Issue reported. Moving to maintenance.")
            self.set_state(FreeMaintenanceState(self))
        elif isinstance(self.state, OccupiedState):
            print("Issue reported. Moving to maintenance.")
            self.set_state(OccupiedMaintenanceState(self))
        elif isinstance(self.state, OccupiedMaintenanceState):
            raise Exception("Already under maintenance.")
        elif isinstance(self.state, FreeMaintenanceState):
            raise Exception("Already under maintenance.")
    
    def finish_maintenance(self):
        if isinstance(self.state, FreeState):
            raise Exception("Already in a free state.")
        elif isinstance(self.state, OccupiedState):
            raise Exception("Cannot finish maintenance in occupied state.")
        elif isinstance(self.state, FreeMaintenanceState):
            print("Maintenance finished. Moving to free state.")
            self.set_state(FreeState(self))
        elif isinstance(self.state, OccupiedMaintenanceState):
            print("Maintenance finished. Moving to occupied state.")
            self.set_state(OccupiedState(self))


# State Classes
class StallState(ABC):
    def __init__(self, stall):
        self.stall = stall


class FreeState(StallState):
    def __init__(self, stall):
        super().__init__(stall)
    

class OccupiedState(StallState):
    def __init__(self, stall):
        super().__init__(stall)


class FreeMaintenanceState(StallState):
    def __init__(self, stall):
        super().__init__(stall)


class OccupiedMaintenanceState(StallState):
    def __init__(self, stall):
        super().__init__(stall)
